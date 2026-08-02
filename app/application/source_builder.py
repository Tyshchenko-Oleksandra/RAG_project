from app.domain.models import RetrievedChunk


class SourceBuilder:
    """Перетворює metadata знайдених chunks на список джерел."""

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[dict]:
        sources = []

        for chunk in chunks:
            metadata = chunk.metadata

            source_info = {
                "source": metadata.get("source"),
                "subject": metadata.get("subject"),
                "content_type": metadata.get("content_type"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": chunk.distance,
            }

            if metadata.get("page") is not None:
                source_info["page"] = metadata["page"]
                source_info["label"] = (
                    f'{metadata.get("source")}, '
                    f'сторінка {metadata["page"]}'
                )

            elif metadata.get("slide") is not None:
                source_info["slide"] = metadata["slide"]
                source_info["label"] = (
                    f'{metadata.get("source")}, '
                    f'слайд {metadata["slide"]}'
                )

            else:
                source_info["label"] = (
                    f'{metadata.get("source")}, '
                    f'chunk {metadata.get("chunk_index")}'
                )

            sources.append(source_info)

        return sources