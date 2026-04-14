"""Local copy of sequana.laa.Consensus fixed for sequana>=0.18 (VariantFile API).

Kept in the pipeline so the workflow does not depend on an unreleased sequana fix.
"""
import colorlog
import pandas as pd

from sequana.variants import VariantFile

logger = colorlog.getLogger(__name__)


class Consensus:
    def __init__(self, bases, freebayes=None):
        self.filename_bases = bases
        self.min_depth = 10
        self.min_score = 1

        if freebayes is not None:
            v = VariantFile(freebayes)
            self.variants = [v._variant_to_dict(x) for x in v.variants]
        else:
            self.variants = []

    def identify_deletions(self):
        deletions = []
        for variant in self.variants:
            alt = variant["alternative"]
            ref = variant["reference"]
            dp = variant["depth"]
            score = variant["freebayes_score"]

            if score < self.min_score:
                continue
            if dp < self.min_depth:
                continue
            if len(alt) < 1:
                continue
            if len(alt) <= len(ref):
                continue

            deletions.append(variant)
        return deletions

    def get_bases(self, skip_rows=3):
        try:
            df = pd.read_csv(self.filename_bases, sep="\t", skiprows=skip_rows, header=None)
        except pd.errors.ParserError:
            df = pd.read_csv(self.filename_bases, sep="\t", skiprows=5, header=None)

        df.columns = ["Pos", "A", "C", "G", "T", "N", "DEL", "INS"]
        df = df.set_index("Pos")

        indices = df[df.sum(axis=1) < self.min_depth].index
        df.loc[indices] = 0
        df.loc[indices, "N"] = 10000
        return df

    def run(self):
        df = self.get_bases()
        deletions = self.identify_deletions()

        dd = df.apply(lambda x: x.idxmax(), axis=1)

        for d in deletions:
            pos = int(d["position"])
            ref = d["reference"]
            if "".join(dd.loc[pos : pos + len(ref) - 1]) != ref:
                logger.warning(
                    "reference string {} not found in consensus at position {}".format(ref, pos)
                )

        for d in deletions:
            pos = int(d["position"])
            ref = d["reference"]
            alt = d["alternative"]

            dfA = df.loc[0 : pos - 1]

            dfB = df.iloc[0 : len(alt)].copy()
            dfB.index = [pos] * len(dfB)
            dfB *= 0
            for i, nucleotide in enumerate(alt):
                dfB.iloc[i][nucleotide] = 10000

            dfC = df.loc[pos + len(ref) :]

            df = pd.concat([dfA, dfB, dfC])

        df.reset_index(drop=True, inplace=True)

        dd = df.apply(lambda x: x.idxmax(), axis=1)
        return dd

    def save_consensus(self, output, identifier):
        dd = self.run()
        with open(output, "w") as fout:
            data = "".join(dd).replace("DEL", "")
            fout.write(">{}\n{}\n".format(identifier, data))

    def get_population(self, threshold=0.1, Npop=2):
        df = self.get_bases()
        cols = ["A", "C", "G", "T", "N", "DEL"]
        df = df.divide(df[cols].sum(axis=1), axis=0)
        selection = df[(df[cols] > threshold).sum(axis=1) >= 2]
        return selection
