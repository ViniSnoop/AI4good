export function WorkspacePolicy({ client }: {
    client: any;
}): Promise<{
    "tool.execute.before"?: undefined;
    "tool.execute.after"?: undefined;
} | {
    "tool.execute.before": (input: any, output: any) => Promise<void>;
    "tool.execute.after": (input: any, output: any) => Promise<void>;
}>;
