
def normalize(collection):
    # works with pandas Series and numpy arrays
    return collection / collection.sum()


def get_item(frame, index_label, row_index, column):
    # use the index label and row index to find the row, and column to find
    # the column
    return frame.loc[frame[index_label] == row_index, column].item()


def running_average(frame, previous_count, new_frame):
    new_count = previous_count + 1
    return (
        (frame * previous_count + new_frame) / new_count,
        new_count
    )
