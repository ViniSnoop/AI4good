import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

np.random.seed(42)


class MLP:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.layers = []
        prev_size = input_size
        for h in hidden_sizes:
            self.layers.append({
                'W': np.random.randn(prev_size, h) * 0.1,
                'b': np.zeros((1, h))
            })
            prev_size = h
        self.layers.append({
            'W': np.random.randn(prev_size, output_size) * 0.1,
            'b': np.zeros((1, output_size))
        })
        self.history = {
            'weights': [],
            'biases': [],
            'activations': [],
            'z_values': [],
            'gradients_W': [],
            'gradients_b': [],
            'loss': [],
            'accuracy': [],
            'lr': []
        }
        self.activations = None
        self.z_values = None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, X, store=False):
        activations = [X]
        z_values = []
        for layer in self.layers:
            z = activations[-1] @ layer['W'] + layer['b']
            z_values.append(z)
            a = self.sigmoid(z)
            activations.append(a)
        if store:
            self.activations = activations
            self.z_values = z_values
        return activations[-1], activations, z_values

    def backward(self, y, lr=0.1):
        m = self.activations[0].shape[0]
        output = self.activations[-1]
        delta = output - y

        grads_W = []
        grads_b = []

        for i in reversed(range(len(self.layers))):
            grad_W = self.activations[i].T @ delta / m
            grad_b = np.sum(delta, axis=0, keepdims=True) / m

            grads_W.insert(0, grad_W.copy())
            grads_b.insert(0, grad_b.copy())

            self.layers[i]['W'] -= lr * grad_W
            self.layers[i]['b'] -= lr * grad_b

            if i > 0:
                delta = (delta @ self.layers[i]['W'].T) * self.sigmoid_derivative(self.z_values[i-1])

        return grads_W, grads_b

    def train_with_logging(self, X, y, epochs=100, lr=0.1, log_every=1, sample_idx=0):
        self.history = {
            'weights': [],
            'biases': [],
            'activations': [],
            'z_values': [],
            'gradients_W': [],
            'gradients_b': [],
            'loss': [],
            'accuracy': [],
            'lr': []
        }

        X_sample = X[sample_idx:sample_idx+1]
        y_sample = y[sample_idx:sample_idx+1]

        for epoch in range(epochs):
            output, _, _ = self.forward(X, store=True)
            loss = -np.mean(y * np.log(output + 1e-8) + (1 - y) * np.log(1 - output + 1e-8))
            pred = (output > 0.5).astype(int)
            acc = np.mean(pred == y)

            grads_W, grads_b = self.backward(y, lr)

            _, sample_activations, sample_z_values = self.forward(X_sample, store=False)

            if epoch % log_every == 0:
                self.history['weights'].append([layer['W'].copy() for layer in self.layers])
                self.history['biases'].append([layer['b'].copy() for layer in self.layers])
                self.history['activations'].append([a.copy() for a in sample_activations])
                self.history['z_values'].append([z.copy() for z in sample_z_values])
                self.history['gradients_W'].append([g.copy() for g in grads_W])
                self.history['gradients_b'].append([g.copy() for g in grads_b])
                self.history['loss'].append(loss)
                self.history['accuracy'].append(acc)
                self.history['lr'].append(lr)

        return self.history


def generate_heart_data(n_samples=300):
    np.random.seed(42)
    age = np.random.normal(55, 10, n_samples)
    sex = np.random.randint(0, 2, n_samples)
    cp = np.random.randint(0, 4, n_samples)
    trestbps = np.random.normal(130, 20, n_samples)
    chol = np.random.normal(240, 50, n_samples)
    fbs = np.random.randint(0, 2, n_samples)
    restecg = np.random.randint(0, 3, n_samples)
    thalach = np.random.normal(150, 25, n_samples)
    exang = np.random.randint(0, 2, n_samples)
    oldpeak = np.random.exponential(1, n_samples)
    slope = np.random.randint(0, 3, n_samples)
    ca = np.random.randint(0, 4, n_samples)
    thal = np.random.randint(0, 4, n_samples)

    X = np.column_stack([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal])
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)

    risk = (age > 55).astype(float) * 0.3 + (cp == 3).astype(float) * 0.3 + (thalach < 130).astype(float) * 0.2 + (exang == 1).astype(float) * 0.2
    y = (risk > 0.5).astype(int).reshape(-1, 1)

    return X, y


def balance_data(X, y):
    """Oversample classe minoritária para balancear 50/50"""
    class_0 = X[y.flatten() == 0]
    class_1 = X[y.flatten() == 1]
    y_0 = y[y.flatten() == 0]
    y_1 = y[y.flatten() == 1]

    if len(class_1) < len(class_0):
        idx = np.random.choice(len(class_1), len(class_0), replace=True)
        class_1_bal = class_1[idx]
        y_1_bal = y_1[idx]
        X_bal = np.vstack([class_0, class_1_bal])
        y_bal = np.vstack([y_0, y_1_bal])
    else:
        idx = np.random.choice(len(class_0), len(class_1), replace=True)
        class_0_bal = class_0[idx]
        y_0_bal = y_0[idx]
        X_bal = np.vstack([class_0_bal, class_1])
        y_bal = np.vstack([y_0_bal, y_1])

    perm = np.random.permutation(len(X_bal))
    return X_bal[perm], y_bal[perm]


def plot_network_animated(mlp, history, epoch_idx, sample_idx=0, max_neurons_per_layer=16):
    if epoch_idx >= len(history['weights']):
        epoch_idx = len(history['weights']) - 1

    weights_at_epoch = history['weights'][epoch_idx]
    biases_at_epoch = history['biases'][epoch_idx]
    activations_at_epoch = history['activations'][epoch_idx]

    layer_sizes = [13] + [w.shape[1] for w in weights_at_epoch]
    n_layers = len(layer_sizes)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-0.5, n_layers + 0.5)
    ax.set_ylim(-0.5, max(layer_sizes) + 0.5)
    ax.axis('off')

    cmap_act = matplotlib.colormaps['RdBu_r']
    cmap_weight = matplotlib.colormaps['RdBu']

    max_w = max(np.max(np.abs(w)) for w in weights_at_epoch) if weights_at_epoch else 1.0
    max_w = max(max_w, 1e-8)

    neuron_positions = []
    for i, size in enumerate(layer_sizes):
        x = i
        display_size = min(size, max_neurons_per_layer)
        y_positions = np.linspace(0, max(layer_sizes) - 1, display_size) if display_size > 1 else [max(layer_sizes) / 2]
        neuron_positions.append((x, y_positions, size, display_size))

    for layer_idx, (x, y_positions, true_size, disp_size) in enumerate(neuron_positions):
        acts = activations_at_epoch[layer_idx][0] if layer_idx < len(activations_at_epoch) else np.zeros(true_size)
        acts_disp = acts[:disp_size] if true_size > disp_size else acts

        for j, y in enumerate(y_positions):
            act_val = acts_disp[j] if j < len(acts_disp) else 0.0
            color = cmap_act(act_val)
            circle = plt.Circle((x, y), 0.35, color=color, ec='black', lw=1.5, zorder=5)
            ax.add_patch(circle)

            if true_size <= max_neurons_per_layer:
                ax.text(x, y, f'{act_val:.2f}', ha='center', va='center', fontsize=8, fontweight='bold', color='white' if act_val > 0.5 else 'black')

        if true_size > max_neurons_per_layer:
            ax.text(x, -0.3, f'... ({true_size} neurônios)', ha='center', fontsize=8, color='gray')

        label = 'Entrada\n(13 features)' if layer_idx == 0 else ('Saída\n(Risco)' if layer_idx == n_layers - 1 else f'Oculta {layer_idx}\n({true_size} neurônios)')
        ax.text(x, -1.2, label, ha='center', fontsize=10, fontweight='bold')

    for layer_idx in range(n_layers - 1):
        x1, y_pos1, true_size1, disp_size1 = neuron_positions[layer_idx]
        x2, y_pos2, true_size2, disp_size2 = neuron_positions[layer_idx + 1]

        W = weights_at_epoch[layer_idx]
        W_disp = W[:disp_size1, :disp_size2] if true_size1 > disp_size1 or true_size2 > disp_size2 else W

        for i, y1 in enumerate(y_pos1):
            for j, y2 in enumerate(y_pos2):
                w = W_disp[i, j] if i < W_disp.shape[0] and j < W_disp.shape[1] else 0.0
                norm_w = w / max_w
                color = cmap_weight(0.5 + 0.5 * np.clip(norm_w, -1, 1))
                alpha = 0.2 + 0.6 * min(abs(norm_w), 1.0)
                lw = 0.3 + 2.5 * min(abs(norm_w), 1.0)

                ax.plot([x1 + 0.35, x2 - 0.35], [y1, y2], color=color, alpha=alpha, lw=lw, zorder=1)

    sm_act = plt.cm.ScalarMappable(cmap=cmap_act, norm=plt.Normalize(0, 1))
    sm_act.set_array([])
    cbar_act = fig.colorbar(sm_act, ax=ax, shrink=0.5, aspect=20, pad=0.02)
    cbar_act.set_label('Ativação (Sigmoid)', fontsize=10)

    sm_w = plt.cm.ScalarMappable(cmap=cmap_weight, norm=plt.Normalize(-max_w, max_w))
    sm_w.set_array([])
    cbar_w = fig.colorbar(sm_w, ax=ax, shrink=0.5, aspect=20, pad=0.02)
    cbar_w.set_label('Peso', fontsize=10)

    epoch_real = epoch_idx * (len(history['loss']) > 1 and (history['loss'].__len__() - 1) // (len(history['weights']) - 1) or 1)
    ax.set_title(f'MLP - Época {epoch_real} | Loss: {history["loss"][epoch_idx]:.4f} | Acc: {history["accuracy"][epoch_idx]:.4f}', fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def plot_metrics_realtime(history, current_epoch_idx):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    epochs_logged = np.arange(len(history['loss'])) * (1 if len(history['loss']) <= 1 else 1)

    ax1 = axes[0, 0]
    ax1.plot(epochs_logged, history['loss'], 'b-', lw=2, label='Loss')
    ax1.axvline(x=current_epoch_idx, color='red', linestyle='--', lw=2, label=f'Época atual')
    ax1.set_xlabel('Época (logada)')
    ax1.set_ylabel('Binary Cross-Entropy')
    ax1.set_title('Loss ao longo do Treinamento')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2 = axes[0, 1]
    ax2.plot(epochs_logged, history['accuracy'], 'g-', lw=2, label='Acurácia')
    ax2.axvline(x=current_epoch_idx, color='red', linestyle='--', lw=2)
    ax2.set_xlabel('Época (logada)')
    ax2.set_ylabel('Acurácia')
    ax2.set_title('Acurácia ao longo do Treinamento')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3 = axes[1, 0]
    if history['gradients_W']:
        grad_norms = []
        for gw in history['gradients_W']:
            total_norm = np.sqrt(sum(np.sum(g**2) for g in gw))
            grad_norms.append(total_norm)
        ax3.plot(epochs_logged, grad_norms, 'r-', lw=2)
        ax3.axvline(x=current_epoch_idx, color='red', linestyle='--', lw=2)
    ax3.set_xlabel('Época (logada)')
    ax3.set_ylabel('||Gradiente||')
    ax3.set_title('Norma do Gradiente (todas camadas)')
    ax3.grid(True, alpha=0.3)

    ax4 = axes[1, 1]
    if history['weights']:
        w = history['weights'][current_epoch_idx][0]
        ax4.hist(w.flatten(), bins=30, color='purple', alpha=0.7, edgecolor='black')
        ax4.axvline(x=0, color='black', linestyle='-', lw=1)
    ax4.set_xlabel('Valor do Peso')
    ax4.set_ylabel('Frequência')
    ax4.set_title(f'Distribuição Pesos Camada 1 (Época {current_epoch_idx})')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_weight_heatmaps(history, epoch_idx):
    weights = history['weights'][epoch_idx]
    n_layers = len(weights)

    fig, axes = plt.subplots(1, n_layers, figsize=(4 * n_layers, 4))
    if n_layers == 1:
        axes = [axes]

    for i, W in enumerate(weights):
        ax = axes[i]
        im = ax.imshow(W.T, aspect='auto', cmap='RdBu', vmin=-np.max(np.abs(W)), vmax=np.max(np.abs(W)))
        ax.set_title(f'Camada {i+1}\n{W.shape[0]}→{W.shape[1]}')
        ax.set_xlabel('Entrada')
        ax.set_ylabel('Saída')
        plt.colorbar(im, ax=ax, shrink=0.8)

    plt.tight_layout()
    return fig


def main():
    st.set_page_config(page_title="MLP Heart Disease - Visual Trainer", layout="wide")

    st.title("🫀 MLP Visual Trainer - Doença Cardíaca")
    st.markdown("**Implementação do zero** com visualização passo a passo de neurônios, pesos e gradientes")

    with st.sidebar:
        st.header("⚙️ Configuração da Rede")
        hidden_layers = st.slider("Camadas ocultas", 1, 3, 2)
        hidden_sizes = []
        for i in range(hidden_layers):
            size = st.slider(f"Neurônios camada {i+1}", 4, 32, 16, key=f"h{i}")
            hidden_sizes.append(size)

        st.divider()
        st.header("🎯 Treinamento")
        epochs = st.slider("Épocas totais", 10, 500, 100, step=10)
        lr = st.select_slider("Learning Rate", [0.01, 0.05, 0.1, 0.2, 0.5], value=0.1)
        log_every = st.select_slider("Log a cada N épocas", [1, 2, 5, 10, 20], value=1)
        sample_idx = st.slider("Amostra para visualização", 0, 299, 0)

        train_btn = st.button("🚀 Treinar e Logar Histórico", type="primary", use_container_width=True)

        if 'history' in st.session_state:
            max_logged = len(st.session_state['history']['loss']) - 1
            epoch_slider = st.slider("Época visualizada", 0, max_logged, 0, key="epoch_slider")

    if train_btn:
        with st.spinner("Gerando dados e treinando com logging completo..."):
            X, y = generate_heart_data(300)
            split = int(0.8 * len(X))
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            X_train, y_train = balance_data(X_train, y_train)

            mlp = MLP(13, hidden_sizes, 1)
            history = mlp.train_with_logging(X_train, y_train, epochs=epochs, lr=lr, log_every=log_every, sample_idx=sample_idx)

            test_pred, _, _ = mlp.forward(X_test)
            test_acc = np.mean((test_pred > 0.5).astype(int) == y_test)

            st.session_state['mlp'] = mlp
            st.session_state['history'] = history
            st.session_state['test_acc'] = test_acc
            st.session_state['X_test'] = X_test
            st.session_state['y_test'] = y_test
            st.session_state['sample_idx'] = sample_idx
            st.session_state['anim_playing'] = False
            st.session_state['current_epoch_idx'] = 0

        st.success(f"✅ Treinamento concluído! Acurácia no teste: **{test_acc:.2%}** | {len(history['loss'])} checkpoints logados")

    if 'history' in st.session_state:
        history = st.session_state['history']
        mlp = st.session_state['mlp']
        sample_idx = st.session_state.get('sample_idx', 0)

        max_logged = len(history['loss']) - 1
        epoch_idx = st.slider("Época para visualizar", 0, max_logged, max_logged, key="epoch_view")

        tab1, tab2, tab3 = st.tabs(["🧠 Rede Neural", "📊 Métricas", "🔥 Heatmaps Pesos"])

        with tab1:
            st.subheader(f"Forward Pass - Amostra {sample_idx} - Época {epoch_idx}")
            net_fig = plot_network_animated(mlp, history, epoch_idx, sample_idx)
            st.pyplot(net_fig)

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Loss", f"{history['loss'][epoch_idx]:.4f}")
            col_m2.metric("Acurácia", f"{history['accuracy'][epoch_idx]:.4f}")
            col_m3.metric("LR", f"{history['lr'][epoch_idx]:.3f}")
            if history['gradients_W']:
                grad_norm = np.sqrt(sum(np.sum(g**2) for g in history['gradients_W'][epoch_idx]))
                col_m4.metric("||Grad||", f"{grad_norm:.4f}")

        with tab2:
            st.subheader("Curvas de Treinamento")
            metrics_fig = plot_metrics_realtime(history, epoch_idx)
            st.pyplot(metrics_fig)

        with tab3:
            st.subheader("Distribuição dos Pesos por Camada")
            heatmap_fig = plot_weight_heatmaps(history, epoch_idx)
            st.pyplot(heatmap_fig)


if __name__ == "__main__":
    main()