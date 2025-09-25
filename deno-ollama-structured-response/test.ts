import { assertEquals, assertRejects } from "jsr:@std/assert";
import { queryStructured } from "./main.ts";
import { FakeListChatModel } from "npm:@langchain/core/utils/testing";

Deno.test("happy case for correct schema", async () => {
  const fakeChatModel = new FakeListChatModel({
    responses: [
      JSON.stringify(
        {
          answer: "some answer",
          source: "https://example.com/source",
          source_description: "source description",
        },
      ),
    ],
  });
  const structuredResponse = await queryStructured("", fakeChatModel);
  assertEquals(structuredResponse, {
    answer: "some answer",
    source: "https://example.com/source",
    source_description: "source description",
  });
});

const testCases = [
  {
    missingFields: ["source", "source_description"],
    payload: {
      answer: "some answer",
    },
  },
  {
    missingFields: ["answer", "source_description"],
    payload: {
      source: "https://example.com/source",
    },
  },
  {
    missingFields: ["answer", "source"],
    payload: {
      source_description: "source description",
    },
  },
  {
    missingFields: ["answer"],
    payload: {
      source: "https://example.com/source",
      source_description: "source description",
    },
  },
  {
    missingFields: ["source"],
    payload: {
      answer: "some answer",
      source_description: "source description",
    },
  },
  {
    missingFields: ["source_description"],
    payload: {
      answer: "some answer",
      source: "https://example.com/source",
    },
  },
];

for (const { payload, missingFields } of testCases) {
  Deno.test(`Payload with missing fields: ${missingFields} fails`, async () => {
    const fakeChatModel = new FakeListChatModel({
      responses: [
        JSON.stringify(payload),
      ],
    });
    await assertRejects(
      () => queryStructured("some prompt", fakeChatModel),
      Error,
      "Failed to parse",
    );
  });
}
