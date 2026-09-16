# class AssetLLMService:

#     def ask(self, asset, question):
#         context = {
#             "name": asset.name,
#             "asset_type": asset.asset_type,
#             "serial_number": asset.serial_number,
#             "location": asset.location,
#             "status": asset.status,
#             "installation_date": asset.installation_date,
#         }

#         # Temporary mock response.
#         # Later this method will call the actual LLM provider.
#         return {
#             "question": question,
#             "asset": context,
#             "answer": (
#                 f"The asset '{asset.name}' is currently "
#                 f"{asset.status} and is located at {asset.location}."
#             ),
#         }




import ollama


class AssetLLMService:

    def ask(self, asset, question):

        context = f"""
Asset Name: {asset.name}
Asset Type: {asset.asset_type}
Serial Number: {asset.serial_number}
Location: {asset.location}
Status: {asset.status}
Installation Date: {asset.installation_date}
"""

        prompt = f"""
You are an airport operations assistant.

Answer the user's question using only the asset information
provided below.

Asset Information:
{context}

User Question:
{question}

Rules:
- Use only the provided asset information.
- Do not invent information.
- If the answer is not available, say that the information
  is not available.
"""

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return {
            "question": question,
            "asset_id": asset.id,
            "answer": response["message"]["content"],
        }