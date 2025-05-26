def generate_tags(prompt):
    base = prompt.lower().replace(" for ", " ").replace(" ", "_")
    title = f"{prompt} | Unique T-Shirt Design"
    description = f"Original design featuring {prompt}. Perfect for fans of creative and seasonal fashion."
    
    tags = list(set(prompt.lower().split())) + [
        "tshirt", "graphic", "design", "2025", "gift", "fun", "trendy"
    ]
    return title, description, tags
