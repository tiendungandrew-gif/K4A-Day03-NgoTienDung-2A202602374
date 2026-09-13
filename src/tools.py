"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu số ngày phép còn lại
    {
        "name": "leave_balance_query",
        "description": "Tra cứu số ngày phép còn lại và thông tin sử dụng phép của nhân viên VinFast bằng mã nhân viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên cần tra cứu (ví dụ: 'NV2026001')"
                }
            },
            "required": ["employee_id"]
        }
    },

    # Tool 2: Tạo đơn xin nghỉ phép
    {
        "name": "create_leave_request",
        "description": "Tạo đơn xin nghỉ phép cho nhân viên VinFast.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên tạo đơn (ví dụ: 'NV2026001')"
                },
                "leave_type": {
                    "type": "string",
                    "description": "Loại nghỉ phép (ví dụ: 'annual_leave' cho nghỉ phép năm, 'unpaid_leave' cho nghỉ không lương)"
                },
                "start_date": {
                    "type": "string",
                    "description": "Ngày bắt đầu nghỉ phép (ví dụ: '20/09/2026')"
                },
                "end_date": {
                    "type": "string",
                    "description": "Ngày kết thúc nghỉ phép (ví dụ: '21/09/2026')"
                },
                "reason": {
                    "type": "string",
                    "description": "Lý do xin nghỉ phép (ví dụ: 'việc cá nhân')"
                }
            },
            "required": ["employee_id", "leave_type", "start_date", "end_date", "reason"]
        }
    },

    # Tool 3: Tra cứu chính sách bảo hiểm
    {
        "name": "insurance_policy_query",
        "description": "Tra cứu thông tin và chính sách bảo hiểm (BHXH, BHYT, Bảo hiểm sức khỏe) của VinFast.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Từ khóa hoặc câu hỏi cần tra cứu chính sách bảo hiểm (ví dụ: 'bhxh', 'bảo hiểm sức khỏe')"
                }
            },
            "required": ["query"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# ==========================================
# 1. MOCK DATABASE - Dữ liệu nhân sự VinFast
# ==========================================

MOCK_DATABASE = {
    "NV2026001": {
        "full_name": "Nguyễn Văn An",
        "department": "AI Engineering",
        "email": "an.nv@vinfast.vn",
        "position": "AI Engineer",
        "status": "Đang làm việc",
        "leave_balance": {
            "annual_leave": 12,
            "used_leave": 4,
            "remaining_leave": 8
        }
    },
    "NV2026002": {
        "full_name": "Trần Thị Bình",
        "department": "Human Resources",
        "email": "binh.tt@vinfast.vn",
        "position": "HR Specialist",
        "status": "Đang làm việc",
        "leave_balance": {
            "annual_leave": 12,
            "used_leave": 6,
            "remaining_leave": 6
        }
    }
}


# ==========================================
# 2. MOCK DATABASE - Chính sách bảo hiểm
# ==========================================

INSURANCE_POLICIES = {
    "bhxh": {
        "title": "Bảo hiểm xã hội",
        "content": (
            "Nhân viên được tham gia bảo hiểm xã hội "
            "theo quy định pháp luật và chính sách của công ty."
        )
    },
    "bhyt": {
        "title": "Bảo hiểm y tế",
        "content": (
            "Nhân viên được tham gia bảo hiểm y tế "
            "theo quy định hiện hành."
        )
    },
    "bao_hiem_suc_khoe": {
        "title": "Bảo hiểm sức khỏe",
        "content": (
            "Nhân viên được hưởng quyền lợi bảo hiểm sức khỏe "
            "theo chính sách và điều kiện áp dụng của công ty."
        )
    }
}


# ==========================================
# 3. Tra cứu ngày phép còn lại
# ==========================================

def execute_leave_balance_query(employee_id: str) -> str:
    """Thực thi tra cứu ngày phép theo mã nhân viên."""

    employee_id = employee_id.strip().upper()
    employee = MOCK_DATABASE.get(employee_id)

    if employee:
        return json.dumps({
            "status": "SUCCESS",
            "employee_id": employee_id,
            "data": {
                "full_name": employee["full_name"],
                "department": employee["department"],
                "leave_balance": employee["leave_balance"]
            }
        }, ensure_ascii=False)

    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu nhân viên có mã '{employee_id}'"
        }, ensure_ascii=False)


# ==========================================
# 4. Tra cứu chính sách bảo hiểm
# ==========================================

def execute_insurance_policy_query(query: str) -> str:
    """Thực thi tra cứu chính sách bảo hiểm."""

    query_lower = query.strip().lower()

    # Tìm chính sách phù hợp dựa trên từ khóa
    matched_policies = []

    for key, policy in INSURANCE_POLICIES.items():
        if (
            key in query_lower
            or policy["title"].lower() in query_lower
        ):
            matched_policies.append(policy)

    if matched_policies:
        return json.dumps({
            "status": "SUCCESS",
            "query": query,
            "data": matched_policies
        }, ensure_ascii=False)

    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": (
                f"Không tìm thấy chính sách bảo hiểm phù hợp với "
                f"câu hỏi '{query}'"
            )
        }, ensure_ascii=False)


# ==========================================
# 5. Tạo đơn xin nghỉ phép
# ==========================================

def execute_create_leave_request(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str
) -> str:
    """Thực thi tạo đơn xin nghỉ phép."""

    employee_id = employee_id.strip().upper()
    employee = MOCK_DATABASE.get(employee_id)

    # Kiểm tra nhân viên tồn tại
    if not employee:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy nhân viên có mã '{employee_id}'"
        }, ensure_ascii=False)

    # Kiểm tra số ngày phép
    remaining_leave = employee["leave_balance"]["remaining_leave"]

    # Mock: Tạm tính số ngày nghỉ dựa trên ngày bắt đầu/kết thúc
    # Trong hệ thống thực tế cần dùng datetime để tính chính xác
    requested_days = 2

    if leave_type == "annual_leave":
        if remaining_leave < requested_days:
            return json.dumps({
                "status": "INSUFFICIENT_LEAVE",
                "message": (
                    f"Nhân viên chỉ còn {remaining_leave} ngày phép, "
                    f"không đủ để nghỉ {requested_days} ngày."
                )
            }, ensure_ascii=False)

    # Mock tạo đơn thành công
    return json.dumps({
        "status": "SUCCESS",
        "request_id": f"LR-{employee_id}-99",
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "requested_days": requested_days,
        "message": (
            f"Tạo đơn xin nghỉ phép thành công cho nhân viên "
            f"{employee_id} từ {start_date} đến {end_date}."
        )
    }, ensure_ascii=False)


# ==========================================
# 6. TOOL ROUTER - Gọi Tool thực tế
# ==========================================

TOOL_ROUTER = {
    "leave_balance_query": execute_leave_balance_query,
    "insurance_policy_query": execute_insurance_policy_query,
    "create_leave_request": execute_create_leave_request
}


# ==========================================
# 7. DISPATCH TOOL CALL
# ==========================================

def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:
    """Hàm trung chuyển thực thi tool."""

    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)

        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }, ensure_ascii=False)

    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại!"
    }, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print(f"✅ [TOOLS CHECK]: Đã đăng ký thành công {len(TOOLS_SCHEMA)} Native Tools trong TOOLS_SCHEMA!")

    if "leave_balance_query" in TOOL_ROUTER:
        test_res = json.loads(dispatch_tool_call("leave_balance_query", {"employee_id": "NV2026001"}))
        name = test_res.get("data", {}).get("full_name", "")
        status = test_res.get("status", "SUCCESS")
        print(f"🧪 Kết quả gọi thử leave_balance_query: Status {status} (Nhân viên {name})")
    elif "academic_query" in TOOL_ROUTER:
        test_res = json.loads(dispatch_tool_call("academic_query", {"student_id": "SV2026001"}))
        name = test_res.get("data", {}).get("full_name", "")
        status = test_res.get("status", "SUCCESS")
        print(f"🧪 Kết quả gọi thử academic_query: Status {status} (Sinh viên {name})")

