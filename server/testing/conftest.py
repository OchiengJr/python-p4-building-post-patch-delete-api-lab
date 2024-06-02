#!/usr/bin/env python3

def pytest_itemcollected(item):
    try:
        # Get the parent and node objects
        parent_obj = item.parent.obj
        node_obj = item.obj

        # Extract the prefix and suffix from parent and node docstrings
        prefix = parent_obj.__doc__.strip() if parent_obj.__doc__ else parent_obj.__class__.__name__
        suffix = node_obj.__doc__.strip() if node_obj.__doc__ else node_obj.__name__

        # Generate the node ID with a formatted prefix and suffix
        if prefix or suffix:
            item._nodeid = ' '.join((prefix, suffix))
    except AttributeError as e:
        # Handle cases where parent_obj or node_obj is None
        print(f"Error processing test item: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
