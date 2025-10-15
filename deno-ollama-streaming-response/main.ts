
import { ChatOllama } from "npm:@langchain/ollama";

const model = new ChatOllama({
    model: "llama3.2:latest",
});

Deno.serve( async (_req) => {
    const inputText = "Give me a 10000 word story about the galaxy";

    const response = await model.stream(inputText);
    const stream = new ReadableStream({
        async start(controller) {
            for await (const chunk of response) {
                controller.enqueue(new TextEncoder().encode(chunk.content));
            }
            controller.close();
        }
    });
    return new Response(stream, {
        headers: {
            "content-type": "text/plain",
            "x-content-type-options": "nosniff",
        }}
    );
});

