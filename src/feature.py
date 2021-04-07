import pandas as pd
import category_encoders as ce
from xfeat import TargetEncoder


class BaseBlock(object):
    def fit(self, input_df: pd.DataFrame, y=None) -> pd.DataFrame:
        return self.transform(input_df)

    def transform(self, input_df: pd.DataFrame) -> pd.DataFrame:
        return NotImplementedError()


class OrdinalEncodingBlock(BaseBlock):
    def __init__(self, cat_cols: list):
        self.cat_cols = cat_cols
        self.encoder = None

    def fit(self, input_df: pd.DataFrame, y=None):
        self.encoder = ce.OrdinalEncoder(handle_unknown="value", handle_missing="value")
        self.encoder.fit(input_df[self.cat_cols])
        return self.transform(input_df)

    def transform(self, input_df: pd.DataFrame):
        return (
            self.encoder.transform(input_df[self.cat_cols])
            .add_prefix("OE_")
            .astype(int)
        )


class CountEncodingBlock(BaseBlock):
    def __init__(self, cat_cols: list):
        self.cat_cols = cat_cols
        self.encoder = None

    def fit(self, input_df: pd.DataFrame, y=None):
        self.encoder = ce.CountEncoder(handle_unknown=-1, handle_missing="count")
        self.encoder.fit(input_df[self.cat_cols])
        return self.transform(input_df)

    def transform(self, input_df: pd.DataFrame):
        return self.encoder.transform(input_df[self.cat_cols]).add_prefix("CE_")


class OneHotEncodingBlock(BaseBlock):
    def __init__(self, cat_cols: list):
        self.cat_cols = cat_cols
        self.encoder = None

    def fit(self, input_df: pd.DataFrame, y=None):
        self.encoder = ce.OneHotEncoder(
            use_cat_names=True, handle_unknown="value", handle_missing="value"
        )
        self.encoder.fit(input_df[self.cat_cols])
        return self.transform(input_df)

    def transform(self, input_df: pd.DataFrame):
        return self.encoder.transform(input_df[self.cat_cols]).add_prefix("OHE_")


class GroupingBlock(BaseBlock):
    def __init__(self, cat_cols: list, target_cols: list, methods: list):
        self.cat_cols = cat_cols
        self.target_cols = target_cols
        self.methods = methods
        self.df = None
        self.a_cat = None

    def fit(self, input_df: pd.DataFrame, y=None):
        self.df = [self._agg(input_df, target_col) for target_col in self.target_cols]
        self.df = pd.concat(self.df, axis=1)
        self.df[self.cat_cols] = self.a_cat[self.cat_cols]

    def transform(self, input_df: pd.DataFrame):
        output_df = pd.merge(
            input_df[self.cat_cols], self.df, on=self.cat_cols, how="left"
        )
        output_df = output_df.drop(columns=self.cat_cols, axis=1)
        return output_df

    def _agg(self, input_df: pd.DataFrame, target_col: str):
        _df = input_df.groupby(self.cat_cols, as_index=False).agg(
            {target_col: self.methods}
        )
        cols = self.cat_cols + [
            f"agg_{method}_{target_col}_by_{'_&_'.join(self.cat_cols)}"
            for method in self.methods
        ]
        _df.columns = cols
        self.a_cat = _df[self.cat_cols]
        return _df.drop(columns=self.cat_cols, axis=1)


class StringLengthBlock(BaseBlock):
    def __init__(self, cat_cols: list):
        self.cat_cols = cat_cols

    def transform(self, input_df: pd.DataFrame):
        output_df = pd.DataFrame()
        for col in self.cat_cols:
            output_df[col] = input_df[col].str.len()

        return output_df.add_prefix("StringLength_")


def text_preprocess(text):


# class TfidfBlock(BaseBlock):
#     def __init__(self)
