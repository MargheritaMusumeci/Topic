from pydantic import BaseModel

class Topic(BaseModel):
    topics: list  = ["Two peas in a pod", "Burning Red", "Bridge", "On the top", "Sweet (dreams)",
                     "Something that made you smile", "Stage", "Gold Rush", "Out of the box", "Shining light", "Home",
                     "Because the night", "Your current obsession"]

    questions: list = ["How do you think the concept of 'two peas in a pod’ manifests in different relationships and connections?",
                       "In what ways do you interpret the metaphorical significance of 'Burning Red’?",
                       "How might the idea of building or crossing bridges influence your understanding of personal growth and interpersonal dynamics?",
                       "How does this concept relate to personal achievements, aspirations, or the pursuit of success?",
                       "How do you believe the notion of sweetness in dreams influences our emotional well-being and perceptions?",
                       "What role do smiles play in your life?",
                       "How do you perceive the significance of a 'stage’ in different contexts?",
                       "In what ways do you see the significance of gold, whether in terms of material wealth, cultural value, or metaphorical representation?",
                       "Tell about an experience where you had to think 'outside the box’ or adopt a creative and innovative approach",
                       "In what unconventional or unexpected ways do you envision 'shining light’?",
                       "How do you personally define the concept of 'Home’?",
                       "Can you share a personal or creative interpretation of the phrase 'because the night’?",
                       "What is currently captivating your attention and sparking enthusiasm in your life?"]

    def get_topic(self, day: str):
        day = int(day)
        return self.topics[day] if 0 <= day < len(self.topics) else None

    def set_topic(self, new_topics: list):
        self.topics += new_topics

    def get_question(self, day: str):
            day = int(day)
            return self.questions[day] if 0 <= day < len(self.questions) else None

    def set_question(self, new_questions: list):
            self.questions += new_questions

    