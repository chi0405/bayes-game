import streamlit as st
import random

st.set_page_config(page_title="Xác Suất Đại Chiến", layout="wide")
st.title("🎲 XÁC SUẤT ĐẠI CHIẾN")

# Khởi tạo trạng thái trò chơi
if 'score' not in st.session_state:
    st.session_state.score = {"Đội A": 0, "Đội B": 0}
    st.session_state.used_questions = {"Đội A": set(), "Đội B": set()}
    st.session_state.current_question = None
    st.session_state.current_options = []
    st.session_state.current_answer = None
    st.session_state.show_answer = False
    st.session_state.game_over = False
    st.session_state.last_difficulty = None
    st.session_state.answered_counts = {"Đội A": 0, "Đội B": 0}
    st.session_state.answer_log = {"Đội A": [], "Đội B": []}

# Danh sách câu hỏi (rút gọn để ví dụ)
questions = [
    {"id": 1, "category": "Xác suất có điều kiện", "level": 1, "question": "Một hộp có 10 thẻ số chẵn. Nếu biết đã lấy thẻ chẵn, xác suất để là số 10 là?", "options": ["1/20", "1/2", "1/10", "1/5"], "answer": "1/10"},
    {"id": 2, "category": "Xác suất có điều kiện", "level": 2, "question": "60% học sinh là nữ. 80% nữ giỏi Toán, 50% nam giỏi Toán. Chọn học sinh giỏi Toán. Xác suất là nữ?", "options": ["0.6", "0.5", "0.8", "0.6957"], "answer": "0.6957"},
    {"id": 3, "category": "Xác suất có điều kiện", "level": 3, "question": "Lớp có 40% chọn A01. Tỉ lệ đậu A01 là 60%, B00 là 80%. Đã đậu, xác suất chọn A01 là?", "options": ["0.4", "0.333", "0.2857", "0.6"], "answer": "0.2857"},
    {"id": 4, "category": "Xác suất toàn phần", "level": 1, "question": "Máy bị lỗi 20%. Nếu lỗi: phát hiện đúng 95%. Không lỗi: dương tính giả 1%. Xác suất bị phát hiện là?", "options": ["0.2", "0.19", "0.058", "0.2"], "answer": "0.058"},
    {"id": 5, "category": "Xác suất toàn phần", "level": 2, "question": "Đơn hàng từ A(50%), B(30%), C(20%). Xác suất đúng hạn: 90%, 80%, 70%. Xác suất giao đúng là?", "options": ["0.80", "0.75", "0.83", "0.70"], "answer": "0.83"},
    {"id": 6, "category": "Bayes & thực tế", "level": 3, "question": "Máy bay phát hiện vật thể vùng C. P(C)=0.2, P(A)=0.5, P(B)=0.3. P(đúng|C)=0.9, P(ngộ nhận)=0.2. P(thực ở C)?", "options": ["0.2", "0.4737", "0.9", "0.6"], "answer": "0.4737"},
    {"id": 7, "category": "Xác suất có điều kiện", "level": 1, "question": "Biết một học sinh là học sinh giỏi. Xác suất để em đó giỏi cả Toán và Lý là 0.3, xác suất giỏi Lý là 0.6. Hỏi xác suất em đó giỏi Toán biết rằng giỏi Lý?", "options": ["0.5", "0.3", "0.6", "0.75"], "answer": "0.5"},
    {"id": 8, "category": "Xác suất toàn phần", "level": 2, "question": "Một sản phẩm từ 3 nhà máy A, B, C với tỉ lệ 40%, 40%, 20%. Tỉ lệ đạt: A 90%, B 80%, C 70%. Hỏi xác suất một sản phẩm đạt?", "options": ["0.8", "0.82", "0.83", "0.84"], "answer": "0.82"},
    {"id": 9, "category": "Bayes & thực tế", "level": 3, "question": "Một bệnh rất hiếm, tỉ lệ mắc là 0.1%. Xét nghiệm dương tính đúng 99%, dương tính giả 2%. Hỏi xác suất thật sự mắc bệnh nếu có kết quả dương tính?", "options": ["0.99", "0.5", "0.047", "0.33"], "answer": "0.047"}
]

st.sidebar.header("🎮 Điều khiển trò chơi")
team = st.sidebar.selectbox("Chọn đội chơi:", ["Đội A", "Đội B"])
difficulty = st.sidebar.radio("Chọn mức độ câu hỏi:", [1, 2, 3], format_func=lambda x: {1: "Dễ (1 điểm)", 2: "Vừa (2 điểm)", 3: "Khó (3 điểm)"}[x])

# Hiển thị số lượt còn lại
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Số lượt còn lại:")
for t in ["Đội A", "Đội B"]:
    remaining = 3 - st.session_state.answered_counts[t]
    st.sidebar.write(f"{t}: {remaining} lượt")

# Câu hỏi + Bảng điểm
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h2 style='font-size:30px;'>📌 Câu hỏi</h2>", unsafe_allow_html=True)
    if st.session_state.answered_counts[team] >= 3:
        st.warning(f"🚫 {team} đã hoàn thành 3 câu hỏi!")
    else:
        if st.session_state.last_difficulty != difficulty:
            st.session_state.current_question = None
            st.session_state.current_options = []
            st.session_state.current_answer = None
            st.session_state.show_answer = False
            st.session_state.last_difficulty = difficulty

        available_questions = [q for q in questions if q['level'] == difficulty and q['id'] not in st.session_state.used_questions[team]]

        if not st.session_state.current_question and available_questions:
            q = random.choice(available_questions)
            st.session_state.current_question = q
            st.session_state.current_options = q['options']
            st.session_state.current_answer = q['answer']
            st.session_state.show_answer = False

        if st.session_state.current_question:
            q = st.session_state.current_question
            st.markdown(f"<h3 style='font-size:25px;'>{q['question']}</h3>", unsafe_allow_html=True)

            user_answer = st.radio("Chọn đáp án:", st.session_state.current_options, key=f"answer_{q['id']}_{team}")

            if st.button("✅ Trả lời"):
                st.session_state.show_answer = True
                st.session_state.used_questions[team].add(q['id'])
                st.session_state.answered_counts[team] += 1
                correct = user_answer == q['answer']
                st.session_state.answer_log[team].append({
                    "question": q['question'],
                    "answer": user_answer,
                    "correct_answer": q['answer'],
                    "correct": correct,
                    "points": q['level'] if correct else 0
                })
                if correct:
                    st.success(f"🎉 Chính xác! +{q['level']} điểm cho {team}")
                    st.session_state.score[team] += q['level']
                else:
                    st.error(f"❌ Sai rồi! Đáp án đúng là: {q['answer']}")

            if st.session_state.show_answer:
                if st.button("🔁 Câu hỏi mới"):
                    st.session_state.current_question = None
                    st.session_state.current_options = []
                    st.session_state.current_answer = None
                    st.session_state.show_answer = False

with col2:
    st.markdown("### 📊 Bảng điểm hiện tại")
    st.markdown("<div style='font-size:25px;'>", unsafe_allow_html=True)
    for t, s in st.session_state.score.items():
        st.write(f"{t}: {s} điểm")
    st.markdown("</div>", unsafe_allow_html=True)

# Kết thúc trò chơi
if all(count >= 3 for count in st.session_state.answered_counts.values()):
    st.markdown("---")
    st.success("🎉 Trò chơi kết thúc!")
    winner = max(st.session_state.score, key=st.session_state.score.get)
    st.balloons()
    st.markdown(f"🏆 **Đội chiến thắng là: {winner} với {st.session_state.score[winner]} điểm!**")

    st.markdown("---")
    st.markdown("### 🧩 Tổng kết câu trả lời từng đội")
    for team_name, logs in st.session_state.answer_log.items():
        st.markdown(f"#### 📌 {team_name}")
        for idx, log in enumerate(logs, 1):
            result = "✅ Đúng" if log['correct'] else "❌ Sai"
            st.markdown(f"**Câu {idx}:** {log['question']}  ")
            st.markdown(f"- Trả lời: {log['answer']} ({result})")
            st.markdown(f"- Đáp án đúng: {log['correct_answer']}, Điểm: {log['points']}\n")
