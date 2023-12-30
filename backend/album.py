from pydantic import BaseModel

class Album(BaseModel):
    pictures: dict = {} # day -> picture
    answers: dict = {}
    votes: dict  = {} # day -> (sum, num_votes)
    
    def vote(self, day: str, vote: int):
        if day not in self.votes:
            self.votes[day] = {"sum": vote, "count": 1}
        else:
            self.votes[day]["sum"] += vote
            self.votes[day]["count"] += 1

    def get_vote(self, day: str):
        if day in self.votes and self.votes[day]["count"] > 0:
            return self.votes[day]["sum"] / self.votes[day]["count"]
        return 0
        
    def get_picture(self, day: str):
        return self.pictures.get(day, None)
    
    def set_picture(self, day: str, picture: str):
        self.pictures[day] = picture

    def get_answer(self, day: str):
        return self.answers.get(day, None)

    def set_answer(self, day: str, answer: str):
        self.answers[day] = answer


class Picture(BaseModel):
    username: str
    day: str
    picture: str