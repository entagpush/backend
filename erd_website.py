from graphviz import Digraph

dot = Digraph(comment="Entag Website ERD")

# Define nodes
dot.node("A", "Blog")
dot.node("B", "Post")
dot.node("C", "Category")
dot.node("D", "Tag")
dot.node("E", "Comment")
dot.node("F", "Waitlist")

# Define relationships
dot.edges(["BC", "BD"])  # Post to Category and Tag
dot.edge("B", "E", label="1 to many")  # Post to Comment
dot.edge("C", "B", label="1 to many")  # Category to Post
dot.edge(
    "D", "B", label="many to many", dir="none"
)  # Tag to Post (bidirectional to indicate many to many)

# Attributes for Waitlist
dot.edge(
    "F", "A", label="associated with", style="dotted"
)  # Waitlist to Blog (conceptual link)

# Customize nodes
dot.node("A", "Blog", shape="component")
dot.node("B", "Post", shape="component")
dot.node("C", "Category", shape="component")
dot.node("D", "Tag", shape="component")
dot.node("E", "Comment", shape="component")
dot.node("F", "Waitlist", shape="note")

# Display the graph
dot.format = "png"
path = "/mnt/data/entag_website_erd.png"
dot.render(path, view=False)
