from sklearn.preprocessing import LabelEncoder

from src.db.df_labels.bag_of_words import BagOfWordsBaseLabels
from src.db.dtos.labeled_data_frame import LabeledDataFrame
from src.ml_input_builder.df_labels.bag_of_words.combined import BagOfWordsCombinedLabels
from src.ml_input_builder.dtos.intermediate.bag_of_words import BagOfWordsIntermediate
from src.ml_input_builder.dtos.params.csr_matrix import CSRMatrixParams


class Formatter:

    @staticmethod
    async def bag_of_words(
        ldf: LabeledDataFrame[BagOfWordsBaseLabels]
    ) -> BagOfWordsIntermediate:
        df = ldf.df
        df_labels = BagOfWordsCombinedLabels.from_base(ldf.labels)
        lab_base = df_labels.base
        lab_idx = df_labels.idx

        url_encoder = LabelEncoder()
        term_encoder = LabelEncoder()


        df[lab_idx.url_idx] = url_encoder.fit_transform(df[lab_base.url_id])
        df[lab_idx.term_idx] = term_encoder.fit_transform(df[lab_base.term_id])

        params = CSRMatrixParams(
            data=df[lab_base.tf_idf].to_numpy(),
            row=df[lab_idx.url_idx].to_numpy(),
            col=df[lab_idx.term_idx].to_numpy(),
            shape=(
                df[lab_idx.url_idx].n_unique(),
                df[lab_idx.term_idx].n_unique()
            )
        )

        sparse_matrix = params.to_csr()

        # Extract labels
        df = df.unique(subset=[lab_idx.url_idx]).sort([lab_idx.url_idx])

        return BagOfWordsIntermediate(
            sparse_matrix=sparse_matrix,
            urls_ids=url_encoder.inverse_transform(range(len(url_encoder.classes_))),
            terms_ids=term_encoder.inverse_transform(range(len(term_encoder.classes_))),
            y_relevant=df[lab_base.relevant],
            y_fine=df[lab_base.record_type_fine],
            y_coarse=df[lab_base.record_type_coarse]
        )
