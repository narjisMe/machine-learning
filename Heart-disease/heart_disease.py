import pathlib
import csv

CWD = pathlib.Path(__file__).parent
DATASET_PATH = CWD / "heart+disease"


class HeartDiseaseDataset:

    def _init_(self, path):
        self._path = path
        self._data = []

        with (self._path / "processed.cleveland.data").open(
            "r",
            encoding="utf-8-sig"
        ) as fp:

            reader = csv.reader(fp)

            for row in reader:
                self._add_row(row)


    def _add_row(self, row):
        new_row = []

        for value in row:
            if value == "?":
                new_row.append(None)
            else:
                new_row.append(float(value))

        self._data.append(new_row)


    @property
    def n_rows(self):
        return len(self._data)


    def __str__(self):
        return f"Heart Disease Dataset: {self.n_rows} elements"


    def get_variable(self, column):
        values = []

        for row in self._data:
            values.append(row[column])

        return values

    def mean(self, column):
        values = self.get_variable(column)

        total = 0
        count = 0

        for value in values:
            if value is not None:
                total = total + value
                count = count + 1

        return total / count


dataset = HeartDiseaseDataset(DATASET_PATH)

print(dataset)

ages = dataset.get_variable(0)
print(ages[:10])

print("Age moyen :", dataset.mean(0))