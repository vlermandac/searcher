from typing import List, Set
from pydantic import BaseModel, validator

class Triplet(BaseModel):
subject: str
predicate: str
object: str

@validator('subject', 'predicate', 'object')
def must_not_be_empty(cls, v):
    if not v.strip():
        raise ValueError("Each part of the triplet must be a non-empty
string")
    return v

class KnowledgeGraph(BaseModel):
triplets: Set[Triplet] = set()

def add_triplet(self, subject: str, predicate: str, object: str) ->
None:
    """
    Add a new triplet to the Knowledge Graph.
    """
    triplet = Triplet(subject=subject, predicate=predicate,
object=object)
    self.triplets.add(triplet)

def find_triplets_with_subject(self, subject: str) -> List[Triplet]:
    """
    Retrieve all triplets with the given subject.
    """
    return [triplet for triplet in self.triplets if triplet.subject ==
subject]

def find_triplets_with_object(self, object: str) -> List[Triplet]:
    """
    Retrieve all triplets with the given object.
    """
    return [triplet for triplet in self.triplets if triplet.object ==
object]

def find_triplets_with_predicate(self, predicate: str) ->
List[Triplet]:
    """
    Retrieve all triplets with the given predicate.
    """
    return [triplet for triplet in self.triplets if triplet.predicate
== predicate]

# Example Usage:
if __name__ == "__main__":
kg = KnowledgeGraph()
kg.add_triplet("Socrates", "is", "human")
kg.add_triplet("Plato", "is", "philosopher")
kg.add_triplet("Socrates", "taught", "Plato")

print("Triplets with 'Socrates' as subject:")
for t in kg.find_triplets_with_subject("Socrates"):
    print(t)
