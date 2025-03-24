import streamlit as st
import random

st.set_page_config(page_title="Xác Suất Đại Chiến", layout="centered")
st.title("🎲 XÁC SUẤT ĐẠI CHIẾN")

# Khởi tạo trạng thái trò chơi
if 'score' not in st.session_state:
    st.session_state.score = {"Đội A": 0, "Đội B": 0, "Đội C": 0}
    st.session_state.used_questions = {"Đội A": set(), "Đội B": set(), "Đội C": set()}
    st.session_state.current_question = None
    st.session_state.current_options = []
    st.session_state.current_answer = None
    st.session_state.show_answer = False
    st.session_state.game_over = False
    st.session_state.last_difficulty = None
    st.session_state.answered_counts = {"Đội A": 0, "Đội B": 0, "Đội C": 0}
    st.session_state.answer_log = {"Đội A": [], "Đội B": [], "Đội C": []}

# Danh sách câu hỏi
questions = [
    {"id": 1, "category": "Xác suất có điều kiện", "level": 1, "question": "Một hộp có 10 thẻ số chẵn. Nếu biết đã lấy thẻ chẵn, xác suất để là số 10 là?", "options": ["1/20", "1/2", "1/10", "1/5"], "answer": "1/10"},
    {"id": 2, "category": "Xác suất có điều kiện", "level": 2, "question": "60% học sinh là nữ. 80% nữ giỏi Toán, 50% nam giỏi Toán. Chọn học sinh giỏi Toán. Xác suất là nữ?", "options": ["0.6", "0.5", "0.8", "0.6957"], "answer": "0.6957"},
    {"id": 3, "category": "Xác suất có điều kiện", "level": 3, "question": "Lớp có 40% chọn A01. Tỉ lệ đậu A01 là 60%, B00 là 80%. Đã đậu, xác suất chọn A01 là?", "options": ["0.4", "0.333", "0.2857", "0.6"], "answer": "0.2857"},
    {"id": 4, "category": "Xác suất toàn phần", "level": 1, "question": "Máy bị lỗi 20%. Nếu lỗi: phát hiện đúng 95%. Không lỗi: dương tính giả 1%. Xác suất bị phát hiện là?", "options": ["0.2", "0.19", "0.058", "0.2"], "answer": "0.058"},
    {"id": 5, "category": "Xác suất toàn phần", "level": 2, "question": "Đơn hàng từ A(50%), B(30%), C(20%). Xác suất đúng hạn: 90%, 80%, 70%. Xác suất giao đúng là?", "options": ["0.80", "0.75", "0.83", "0.70"], "answer": "0.83"},
    {"id": 6, "category": "Bayes & thực tế", "level": 3, "question": "Máy bay phát hiện vật thể vùng C. P(C)=0.2, P(A)=0.5, P(B)=0.3. P(đúng|C)=0.9, P(ngộ nhận)=0.2. P(thực ở C)?", "options": ["0.2", "0.4737", "0.9", "0.6"], "answer": "0.4737"},
    {"id": 7, "category": "Xác suất có điều kiện", "level": 1, "question": "Biết một học sinh là học sinh giỏi. Xác suất để em đó giỏi cả Toán và Lý là 0.3, xác suất giỏi Lý là 0.6. Hỏi xác suất em đó giỏi Toán biết rằng giỏi Lý?", "options": ["0.5", "0.3", "0.6", "0.75"], "answer": "0.5"},
    {"id": 8, "category": "Xác suất toàn phần", "level": 2, "question": "Một sản phẩm từ 3 nhà máy A, B, C với tỉ lệ 40%, 40%, 20%. Tỉ lệ đạt: A 90%, B 80%, C 70%. Hỏi xác suất một sản phẩm đạt?", "options": ["0.8", "0.82", "0.83", "0.84"], "answer": "0.82"},
    {"id": 9, "category": "Bayes & thực tế", "level": 3, "question": "Một bệnh rất hiếm, tỉ lệ mắc là 0.1%. Xét nghiệm dương tính đúng 99%, dương tính giả 2%. Hỏi xác suất thật sự mắc bệnh nếu có kết quả dương tính?", "options": ["0.99", "0.5", "0.047", "0.33"], "answer": "0.047"},
    {"id": 10, "category": "Xác suất có điều kiện", "level": 1, "question": "Từ một bộ bài 52 lá, rút ngẫu nhiên một lá, biết rằng lá đó là bích. Xác suất để là quân Át là?", "options": ["1/52", "1/4", "1/13", "1/12"], "answer": "1/13"},
    {"id": 11, "category": "Xác suất toàn phần", "level": 2, "question": "Chuồng I có 5 thỏ đen, 10 thỏ trắng. Chuồng II có 7 thỏ đen, 3 thỏ trắng. Chuyển 1 thỏ ngẫu nhiên từ chuồng II sang I rồi rút từ I. Xác suất lấy được thỏ trắng?", "options": ["0.5", "0.55", "0.6", "0.625"], "answer": "0.625"},
    {"id": 12, "category": "Xác suất toàn phần", "level": 2, "question": "Nhà máy X: 80% sản phẩm đạt chuẩn. Nếu đạt: 0.99 được đóng OTK. Nếu không đạt: 0.05 vẫn bị đóng OTK. Xác suất sản phẩm được đóng dấu OTK?", "options": ["0.8", "0.79", "0.842", "0.814"], "answer": "0.814"},
    {"id": 13, "category": "Xác suất toàn phần", "level": 2, "question": "Đội I có 5 người, mỗi người có xác suất đạt HCV là 0.65. Đội II có 7 người, xác suất đạt HCV là 0.55. Chọn ngẫu nhiên 1 người. Xác suất người đó đạt HCV?", "options": ["0.59", "0.6", "0.575", "0.583"], "answer": "0.583"},
    {"id": 14, "category": "Bayes & thực tế", "level": 3, "question": "Bộ lọc thư rác: chặn 95% thư rác, nhưng 1% thư đúng cũng bị chặn. Tỉ lệ thư rác là 3%. Một thư bị chặn, xác suất nó là thư rác?", "options": ["0.75", "0.5", "0.22", "0.743"], "answer": "0.743"},
    {"id": 15, "category": "Xác suất có điều kiện", "level": 2, "question": "Gieo 2 xúc xắc. Biết có ít nhất 1 xúc xắc ra mặt 5 chấm. Xác suất tổng chấm >= 10 là?", "options": ["0.25", "0.3", "0.33", "0.36"], "answer": "0.36"},
    {"id": 16, "category": "Xác suất toàn phần", "level": 2, "question": "An làm 2 thí nghiệm. Xác suất thành công lần 1 là 0.7. Nếu lần 1 thành công, lần 2 thành công với 0.9; nếu thất bại thì lần 2 thành công 0.4. Xác suất cả hai cùng thành công?", "options": ["0.63", "0.7", "0.5", "0.42"], "answer": "0.63"},
    {"id": 17, "category": "Xác suất toàn phần", "level": 3, "question": "Trong túi có 6 kẹo cam, còn lại là vàng. Hà lấy 2 cái liên tiếp không hoàn lại. Biết xác suất lấy 2 cam là 1/3. Hỏi ban đầu túi có bao nhiêu kẹo?", "options": ["8", "9", "10", "12"], "answer": "9"},
    {"id": 18, "category": "Xác suất có điều kiện", "level": 1, "question": "Từ bộ bài 52 lá, biết đã rút lá cơ. Xác suất rút được lá cơ hình là?", "options": ["1/13", "1/26", "1/4", "1/3"], "answer": "1/13"},
    {"id": 19, "category": "Xác suất toàn phần", "level": 1, "question": "Có 60% học sinh nam, 40% nữ. Nam đến lớp đúng giờ 80%, nữ 90%. Xác suất học sinh bất kỳ đến đúng giờ?", "options": ["0.84", "0.86", "0.88", "0.9"], "answer": "0.84"},
    {"id": 20, "category": "Xác suất có điều kiện", "level": 1, "question": "Biết học sinh tham gia CLB Toán. Xác suất để là học sinh lớp 12 nếu 40% lớp 12 tham gia, toàn trường 20% là lớp 12?", "options": ["0.5", "0.4", "0.2", "0.2857"], "answer": "0.2857"},
    {"id": 21, "category": "Bayes & thực tế", "level": 1, "question": "Một test COVID có độ nhạy 0.95, độ đặc hiệu 0.99. Tỉ lệ F0 là 5%. Xác suất dương tính thật sự là?", "options": ["0.83", "0.75", "0.6", "0.33"], "answer": "0.83"},
    {"id": 22, "category": "Xác suất có điều kiện", "level": 1, "question": "Rút 1 viên bi từ hộp có 5 đỏ, 5 xanh. Biết là bi không đỏ. Xác suất là xanh là?", "options": ["1", "0.5", "5/9", "5/10"], "answer": "1"},
    {"id": 23, "category": "Xác suất toàn phần", "level": 2, "question": "3 máy sản xuất bánh: A (30%), B (50%), C (20%). Xác suất sản phẩm lỗi: A 5%, B 8%, C 10%. Tính xác suất chọn ngẫu nhiên bánh bị lỗi?", "options": ["0.072", "0.065", "0.08", "0.07"], "answer": "0.072"},
    {"id": 24, "category": "Bayes & thực tế", "level": 2, "question": "Tiệm bánh có 3 loại bánh: A (40%), B (35%), C (25%). Bánh A ngon 80%, B 60%, C 50%. Đã ăn ngon, xác suất là bánh A?", "options": ["0.5", "0.47", "0.42", "0.4"], "answer": "0.47"},
    {"id": 25, "category": "Xác suất có điều kiện", "level": 2, "question": "Gieo 2 xúc xắc. Biết có ít nhất một mặt là 6. Tính xác suất tổng là 7?", "options": ["1/11", "1/12", "1/6", "1/9"], "answer": "1/11"},
    {"id": 26, "category": "Xác suất có điều kiện", "level": 2, "question": "Một hộp có 4 bóng đỏ, 6 bóng xanh. Rút 1 bóng không hoàn lại, sau đó rút bóng thứ 2. Xác suất bóng thứ hai là đỏ biết bóng đầu là xanh?", "options": ["4/9", "2/5", "1/2", "4/10"], "answer": "4/9"},
    {"id": 27, "category": "Bayes & thực tế", "level": 2, "question": "Trong kho có 2 loại sản phẩm A (60%), B (40%). A lỗi 2%, B lỗi 5%. Chọn ngẫu nhiên sản phẩm bị lỗi. Xác suất là sản phẩm B?", "options": ["0.5", "0.4", "0.25", "0.526"], "answer": "0.526"},
{"id": 28, "category": "Bayes & thực tế", "level": 3, "question": "Hệ thống phát hiện gian lận online với độ chính xác 98%. Tỉ lệ gian lận thật là 1%. Một trường hợp bị cảnh báo. Xác suất thật sự gian lận?", "options": ["0.33", "0.5", "0.09", "0.327"], "answer": "0.327"},
    {"id": 29, "category": "Xác suất có điều kiện", "level": 3, "question": "Một nhóm có 4 nam, 6 nữ. 3 người được chọn ngẫu nhiên. Biết có ít nhất 2 nữ, xác suất có đủ cả nam và nữ là?", "options": ["0.6", "0.75", "0.85", "0.9"], "answer": "0.75"},
    {"id": 30, "category": "Xác suất toàn phần", "level": 3, "question": "Bệnh viện có 3 khoa. Mỗi khoa có tỉ lệ bệnh nhân khác nhau và xác suất phục hồi khác nhau. Cho bảng dữ liệu. Tính xác suất chọn 1 bệnh nhân phục hồi?", "options": ["0.7", "0.74", "0.78", "0.8"], "answer": "0.74"},
    {"id": 31, "category": "Bayes & thực tế", "level": 3, "question": "Trong hệ thống phát hiện gian lận thẻ, tỉ lệ báo động giả là 1%, tỷ lệ đúng là 90%. Tỉ lệ người gian lận thật là 0.2%. Một báo động xuất hiện. Xác suất đó là gian lận thật?", "options": ["0.15", "0.19", "0.18", "0.1538"], "answer": "0.1538"},
    {"id": 32, "category": "Xác suất có điều kiện", "level": 3, "question": "Có 3 hộp, mỗi hộp chứa số lượng bi đỏ/xanh khác nhau. Chọn ngẫu nhiên 1 hộp, rồi chọn 1 bi. Biết đã rút được bi đỏ. Xác suất lấy từ hộp thứ 1 là?", "options": ["0.3", "0.5", "0.6", "0.4"], "answer": "0.4"}
]

st.sidebar.header("🎮 Điều khiển trò chơi")
team = st.sidebar.selectbox("Chọn đội chơi:", ["Đội A", "Đội B", "Đội C"])
difficulty = st.sidebar.radio("Chọn mức độ câu hỏi:", [1, 2, 3], format_func=lambda x: {1: "Dễ (1 điểm)", 2: "Vừa (2 điểm)", 3: "Khó (3 điểm)"}[x])

# Hiển thị số lượt còn lại
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Số lượt còn lại:")
for t in ["Đội A", "Đội B", "Đội C"]:
    remaining = 6 - st.session_state.answered_counts[t]
    st.sidebar.write(f"{t}: {remaining} lượt")

# Giới hạn 6 câu mỗi đội
if st.session_state.answered_counts[team] >= 6:
    st.warning(f"🚫 {team} đã hoàn thành 6 câu hỏi!")
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
        st.subheader(f"📌 {q['category']} – Mức {q['level']} điểm")
        st.markdown(f"**{q['question']}**")

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

st.markdown("---")
st.markdown("### 📊 Bảng điểm hiện tại")
st.write(st.session_state.score)

if all(count >= 6 for count in st.session_state.answered_counts.values()):
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
