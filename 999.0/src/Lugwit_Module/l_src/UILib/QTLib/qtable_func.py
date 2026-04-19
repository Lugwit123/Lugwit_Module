# coding:utf-8

def adjust_table_height(table):
    height = 0
    for i in range(table.rowCount()):
        height += table.rowHeight(i)
    
    frame_width = table.frameWidth()
    header_height = table.horizontalHeader().height()
    
    # 考虑垂直滚动条的宽度
    if table.verticalScrollBar().isVisible():
        scrollbar_width = table.verticalScrollBar().width()
    else:
        scrollbar_width = 0
    
    table.setFixedHeight(height + header_height + 6 * frame_width + scrollbar_width+3)