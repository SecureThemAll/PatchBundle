# PatchBundle
A Framework for Manipulating Existing Datasets of Security Patches for Automatic Program Repair Techniques and Studies


## Prerequisites

* [Python (=>3.7)](https://www.python.org/)

### Python Dependencies
* [Pandas (>=1.0.3)](https://pandas.pydata.org/)
* [Github](https://pygithub.readthedocs.io/en/latest/introduction.html)


## Baseline

The baseline usage involves three operations: collect, transform and filter.

### Collect
Collect from the specified source the dataset.
The dataset is downloaded to the folder ```PatchBundle/data/collected/'name_of_the_dataset'```

``` console
$ ./tool/PatchBundle.py collect --datasets nvd, mozilla, secretpatch, secbench
```


### Transform
Transforms the collected dataset's records into the PatchRecord format.
The dataset is saved in the folder ```PatchBundle/data/transformed/'name_of_the_dataset'```

``` console
$ ./tool/PatchBundle.py transform --datasets nvd, mozilla, secretpatch, secbench
```

### Filter
Filters the transformed dataset's based on pre-defined decorators in the file ```PatchBundle/tool/decorators/filter.py```.

``` console
$ ./tool/PatchBundle.py filter --datasets nvd, mozilla, secretpatch, secbench
```

Implement your own filter rules and update the filter method in the respective dataset file, ```PatchBundle/tool/datasets/'name_of_the_dataset'.py```.

Example of a custom filter:

``` python
def custom(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dataset = func(*args, **kwargs)
        return dataset.drop(columns=['commit', 'name'])
    return wrapper
```

Add the filter:

``` python
    @save
--> @custom
    @one_line_changes
    @equal_adds_dels
    @c_code
    @load
    def filter(self, path: Path):
        print(f"Filtering {self.name}")
        return self.transformed
```