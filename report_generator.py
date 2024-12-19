# report_generator.py
from database import get_db_connection

def generate_report():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT book_name, COUNT(*) AS borrow_count
        FROM borrows
        GROUP BY book_name
        ORDER BY borrow_count DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    
    # In báo cáo thống kê
    print("Thống kê số lượng sách được mượn nhiều nhất:")
    for row in result:
        print(f"Sách: {row[0]}, Số lần mượn: {row[1]}")
    
    cursor.close()
    connection.close()
