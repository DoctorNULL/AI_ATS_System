class ATSConfig:
    def __init__(self,
                 text_spliter_chunk_size = 100,
                 text_spliter_chunk_overlap = 20,
                 text_similarity_threshold = 0.9,
                 title_similarity_threshold = 0.85
                 ):

        self.text_spliter_chunk_size = text_spliter_chunk_size
        self.text_spliter_chunk_overlap = text_spliter_chunk_overlap
        self.text_similarity_threshold = text_similarity_threshold
        self.title_similarity_threshold = title_similarity_threshold
