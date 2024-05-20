# save-return

Save the return value of the decorated function to a versioned pickle file.

## Save

```python
import save_return

@save_return.save('value_of_pi')
def calc_pi():
    return 4

pi = calc_pi()
```

This will `pickle.dump` `pi` to `{save_dir}/value_of_pi/yyyymmdd_HHMMSS_MS_00000.pkl`.

Run the above code again will save `pi` to `{save_dir}/value_of_pi/yyyymmdd_HHMMSS_MS_00001.pkl`.

- If run inside of a Jupyter notebook, `{save_dir}` defaults to `data/save_return/{notebook_basename}.var`
- Otherwise, it defaults to `data/save_return`
- Use `@save_return.save(..., save_dir="some-dir")` to customize the save location

## Load

The `load` function is just a wrapper around `pickle` to save you some `open()`:

```python
pi = save_return.load('./data/save_return/value_of_pi/yyyymmdd_HHMMSS_MS_00000.pkl')
```