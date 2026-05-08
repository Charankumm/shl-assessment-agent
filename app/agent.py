from app.retriever import SHLRetriever
from app.llm import generate_response

retriever = SHLRetriever()


class SHLAgent:

    def chat(self, messages):

        full_context = self.build_context(messages)

        latest_message = messages[-1]["content"]

        # Refuse off-topic or prompt injection attempts
        if self.is_off_topic(latest_message):

            return {
                "reply": (
                    "I can only help with SHL assessment "
                    "recommendations and comparisons."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Compare assessments
        if self.is_comparison(latest_message):

            results = retriever.search(
                latest_message,
                top_k=2
            )

            recommendations = []

            for r in results:

                recommendations.append({
                    "name": r["name"],
                    "url": r["url"],
                    "test_type": r["test_type"]
                })

            comparison_prompt = f"""
            User query:
            {latest_message}

            SHL assessments:
            {recommendations}

            Compare these assessments briefly.

            Mention:
            - differences in focus
            - skills evaluated
            - hiring use cases

            Keep response under 100 words.
            """

            reply = generate_response(
                comparison_prompt
            )

            return {
                "reply": reply,
                "recommendations": recommendations,
                "end_of_conversation": False
            }

        # Clarification for vague queries
        if self.is_vague(latest_message):

            clarification_prompt = f"""
            User message:
            {latest_message}

            Ask one concise clarification question
            to better understand hiring needs.

            Keep response under 40 words.
            """

            reply = generate_response(
                clarification_prompt
            )

            return {
                "reply": reply,
                "recommendations": [],
                "end_of_conversation": False
            }

        # Retrieve recommendations
        results = retriever.search(
            full_context,
            top_k=5
        )

        recommendations = []

        for r in results:

            recommendations.append({
                "name": r["name"],
                "url": r["url"],
                "test_type": r["test_type"]
            })

        recommendation_prompt = f"""
        User hiring requirements:
        {full_context}

        Recommended SHL assessments:
        {recommendations}

        Explain:
        - why these assessments fit
        - what skills they evaluate
        - how they support hiring decisions

        Mention technical, behavioral,
        leadership, or communication
        evaluation where relevant.

        Keep response under 80 words.
        """

        reply = generate_response(
            recommendation_prompt
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    def build_context(self, messages):

        context = []

        for msg in messages:

            role = msg["role"]
            content = msg["content"]

            context.append(
                f"{role}: {content}"
            )

        return "\n".join(context)

    def is_vague(self, text):

        text = text.lower()

        vague_phrases = [
            "assessment",
            "need assessment",
            "need test",
            "hiring"
        ]

        return (
            len(text.split()) < 4
            or text in vague_phrases
        )

    def is_off_topic(self, text):

        text = text.lower()

        blocked = [
            "salary",
            "tax",
            "bitcoin",
            "movie",
            "football",
            "weather",
            "ignore previous instructions",
            "system prompt",
            "jailbreak",
            "bypass"
        ]

        return any(
            word in text
            for word in blocked
        )

    def is_comparison(self, text):

        text = text.lower()

        comparison_words = [
            "compare",
            "difference",
            "vs",
            "versus"
        ]

        return any(
            word in text
            for word in comparison_words
        )

    def is_refinement(self, text):

        text = text.lower()

        refinement_words = [
            "also",
            "add",
            "include",
            "actually",
            "more"
        ]

        return any(
            word in text
            for word in refinement_words
        )