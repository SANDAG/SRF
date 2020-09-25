
def get_item(frame, index_label, row_index, column):
    # use the index label and row index to find the row, and column to find
    # the column
    return frame.loc[frame[index_label] == row_index, column].item()
