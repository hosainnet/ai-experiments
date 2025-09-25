import { ChatOllama } from "npm:@langchain/ollama";

import { z } from "npm:zod";
import { RunnableSequence } from "npm:@langchain/core/runnables";
import { StructuredOutputParser } from "npm:@langchain/core/output_parsers";
import { ChatPromptTemplate } from "npm:@langchain/core/prompts";
import { BaseChatModel } from "npm:@langchain/core";

const zodSchema = z.object({
  answer: z.string().describe("answer to the user's question"),
  source: z.string().describe(
    "source used to answer the user's question, should be a website.",
  ),
  source_description: z.string().describe(
    "description of the source used to answer the user's question.",
  ),
});

export const queryStructured = async (prompt: string, model: BaseChatModel) => {
  const parser = StructuredOutputParser.fromZodSchema(zodSchema);

  const chain = RunnableSequence.from([
    ChatPromptTemplate.fromTemplate(
      "Answer the users question as best as possible.\n{format_instructions}\n{question}",
    ),
    model,
    parser,
  ]);

  return await chain.invoke({
    question: prompt,
    format_instructions: parser.getFormatInstructions(),
  });
};

if (import.meta.main) {
  const model = new ChatOllama({
    model: Deno.args[0],
  });
  const structuredResponse = await queryStructured("What is a Deno?", model);
  console.log(structuredResponse);
}
