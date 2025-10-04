import streamlit as st
import yfinance as yf
import random
import json

def generate_educational_response(question, all_questions):
    """Generate educational responses based on the user's question"""
    question_lower = question.lower()
    
    # Budgeting and 30% rule
    if any(keyword in question_lower for keyword in ['30%', 'rent', 'budget', 'housing', 'rule']):
        return """<h3>🏠 The 30% Rule for Housing Costs</h3>

<p>The 30% rule is a widely recommended guideline that suggests you should spend no more than 30% of your gross monthly income on housing costs (rent or mortgage payments).</p>

<h4>Why this matters:</h4>

<ul>
<li><strong>Financial Stability</strong>: Keeps housing affordable relative to your income</li>
<li><strong>Emergency Fund</strong>: Leaves room for savings and unexpected expenses</li>
<li><strong>Other Expenses</strong>: Ensures you can cover food, transportation, healthcare, and other necessities</li>
<li><strong>Debt Management</strong>: Prevents overextending yourself financially</li>
</ul>

<h4>Example:</h4>

<p>If you earn $3,000/month, your housing costs should be $900 or less.</p>

<p><strong>Pro tip:</strong> This includes rent/mortgage, utilities, insurance, and property taxes. Some experts suggest 25% for even better financial health!</p>"""

    # APR explanation
    elif any(keyword in question_lower for keyword in ['apr', 'interest', 'rate', 'annual percentage']):
        return """💳 **Understanding APR (Annual Percentage Rate)**

APR stands for Annual Percentage Rate - it's the yearly cost of borrowing money, expressed as a percentage.

**What APR includes:**
• Interest rate on the loan
• Fees and charges
• Other costs associated with the loan

**Why APR matters:**
• **True Cost**: Shows the real cost of borrowing, not just the interest rate
• **Comparison Tool**: Helps you compare different loan offers
• **Budget Planning**: Helps you understand your monthly payments

**Example**: A credit card with 18% APR means you'll pay $18 in interest for every $100 you borrow for a full year.

**Pro tip**: Lower APR = less money you pay back. Always shop around for the best APR!"""

    # Stock investing
    elif any(keyword in question_lower for keyword in ['stock', 'invest', 'investment', 'diversification', 'portfolio']):
        return """📈 **Stock Investing Fundamentals**

**What are stocks?**
Stocks represent ownership shares in a company. When you buy stock, you become a partial owner.

**Key Concepts:**
• **Risk vs Return**: Higher potential returns usually come with higher risk

• **Diversification**: Don't put all your money in one stock - spread it across different companies and sectors

• **Long-term Thinking**: Stock prices fluctuate daily, but historically, markets tend to rise over time

• **Research**: Always research companies before investing

**Why diversification matters:**
• Reduces risk by spreading investments across different assets

• If one stock performs poorly, others may perform well

• Helps protect your portfolio from major losses

**Pro tip**: Start with index funds or ETFs for instant diversification, then consider individual stocks as you learn more!"""

    # General financial literacy
    elif any(keyword in question_lower for keyword in ['save', 'saving', 'money', 'financial', 'finance']):
        return """💰 **Financial Literacy Basics**

**Essential Financial Skills:**
• **Budgeting**: Track income and expenses to live within your means
• **Saving**: Build an emergency fund (3-6 months of expenses)
• **Investing**: Make your money work for you over time
• **Debt Management**: Understand good vs bad debt
• **Credit**: Build and maintain good credit scores

**The 50/30/20 Rule:**
• 50% for needs (housing, food, utilities)
• 30% for wants (entertainment, dining out)
• 20% for savings and debt repayment

**Emergency Fund Priority:**
Before investing, build an emergency fund. This protects you from unexpected expenses without going into debt.

**Pro tip**: Start small and be consistent. Even $25/month adds up over time!"""

    # Default response
    else:
        return """🤖 **Financial Learning Assistant**

I'm here to help you understand financial concepts! Here are some topics I can explain:

• **Budgeting**: 30% rule, 50/30/20 rule, emergency funds
• **Credit**: APR, credit scores, debt management
• **Investing**: Stocks, diversification, risk vs return
• **Saving**: Building wealth, compound interest
• **General Finance**: Financial planning, money management

Try asking about any of these topics, or use the quick question buttons above for instant explanations!

**Example questions:**
- "Why is the 30% rule important?"
- "What's the difference between APR and interest rate?"
- "How does compound interest work?"
- "What is diversification in investing?" """

st.title("Financial Literacy Quiz")
st.write("Welcome to the Financial Literacy Quiz! Test your knowledge and learn more about managing your finances.")
st.write("This quiz covers topics such as budgeting, saving, investing, and credit management.")

# Use session state to track quiz state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "all_questions" not in st.session_state:
    st.session_state.all_questions = []

# Step 1: Get user's name
if not st.session_state.quiz_started:
    name = st.text_input("Type in your name:")
    
    if name:
        st.session_state.user_name = name
        st.write(f"Hello {name}. If you're ready, hit start quiz")
        
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            
            # Generate questions once when quiz starts
            static_questions = [
                {
                    "question": "If you earn $2000/month, how much should you ideally spend on rent (30% rule)?",
                    "options": ["$400", "$600", "$800", "$1000"],
                    "answer": "$600"
                },
                {
                    "question": "What does APR stand for?",
                    "options": ["Annual Percentage Rate", "Annual Profit Rate", "Asset Price Return", "Average Payment Ratio"],
                    "answer": "Annual Percentage Rate"
                }
            ]

            # Dynamic question using yfinance
            tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
            ticker = random.choice(tickers)
            try:
                data = yf.download(ticker, period="1y", progress=False)
                if not data.empty and 'Close' in data.columns:
                    start_price = float(data['Close'].iloc[0])
                    end_price = float(data['Close'].iloc[-1])
                    change = ((end_price - start_price) / start_price) * 100
                    
                    # Calculate the final value and ensure it's a proper float
                    final_value = 100 * (1 + change/100)
                    final_value_rounded = round(final_value)
                    
                    stock_question = {
                        "question": f"If you invested $100 in {ticker} a year ago, approximately how much is it worth now?",
                        "options": [f"${final_value_rounded}", "$110", "$120", "$130"],
                        "answer": f"${final_value_rounded}"
                    }
                else:
                    # Fallback question if data download fails
                    stock_question = {
                        "question": "What is the primary purpose of diversification in investing?",
                        "options": ["To increase returns", "To reduce risk", "To avoid taxes", "To time the market"],
                        "answer": "To reduce risk"
                    }
            except Exception as e:
                # Fallback question if yfinance fails
                stock_question = {
                    "question": "What is the primary purpose of diversification in investing?",
                    "options": ["To increase returns", "To reduce risk", "To avoid taxes", "To time the market"],
                    "answer": "To reduce risk"
                }

            # Store all questions in session state
            st.session_state.all_questions = static_questions + [stock_question]
            st.rerun()

# Step 2: Show quiz questions
if st.session_state.quiz_started:
    st.write(f"Hello {st.session_state.user_name}! Let's get started with the quiz.")
    
    # Use the questions stored in session state
    all_questions = st.session_state.all_questions
    
    # Display current question
    if st.session_state.current_question < len(all_questions):
        current_q = all_questions[st.session_state.current_question]
        
        st.subheader(f"Question {st.session_state.current_question + 1}")
        st.write(current_q["question"])
        
        # Display options
        selected_option = st.radio(
            "Choose your answer:",
            current_q["options"],
            key=f"question_{st.session_state.current_question}"
        )
        
        # Next question button
        if st.button("Next Question"):
            st.session_state.user_answers.append(selected_option)
            st.session_state.current_question += 1
            st.rerun()
    
    # Show results when all questions are answered
    else:
        st.subheader("Quiz Complete!")
        st.write(f"Great job, {st.session_state.user_name}!")
        
        # Calculate score
        correct_answers = 0
        for i, answer in enumerate(st.session_state.user_answers):
            if i < len(all_questions) and answer == all_questions[i]["answer"]:
                correct_answers += 1
        
        score = (correct_answers / len(all_questions)) * 100
        st.write(f"Your score: {correct_answers}/{len(all_questions)} ({score:.1f}%)")
        
        # Show correct answers
        st.subheader("Review:")
        for i, question in enumerate(all_questions):
            # Check if user has an answer for this question
            if i < len(st.session_state.user_answers):
                user_answer = st.session_state.user_answers[i]
                correct_answer = question["answer"]
                is_correct = user_answer == correct_answer
                
                st.write(f"**Question {i+1}:** {question['question']}")
                st.write(f"Your answer: {user_answer} {'✅' if is_correct else '❌'}")
                if not is_correct:
                    st.write(f"Correct answer: {correct_answer}")
            else:
                # User didn't answer this question
                st.write(f"**Question {i+1}:** {question['question']}")
                st.write(f"Your answer: Not answered ❌")
                st.write(f"Correct answer: {question['answer']}")
            st.write("---")
        
        # Educational Chatbot Section
        st.subheader("🤖 Financial Learning Assistant")
        st.write("Ask me about any question you got wrong, and I'll explain the concept in detail!")
        
        # Initialize chatbot state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat input
        user_question = st.text_input("Ask about any financial concept (e.g., 'Why is the 30% rule important?' or 'What does APR mean?'):")
        
        if user_question:
            # Add user question to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Generate educational response
            bot_response = generate_educational_response(user_question, all_questions)
            st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("💬 Chat History")
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.write(f"**You:** {message['content']}")
                else:
                    st.write(f"**Learning Assistant:**")
                    # Use st.markdown with unsafe_allow_html for better formatting
                    st.markdown(message['content'], unsafe_allow_html=True)
                st.write("---")
        
        # Quick question buttons
        st.subheader("Quick Questions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Explain 30% Rule"):
                st.session_state.chat_history.append({"role": "user", "content": "Explain the 30% rule for rent"})
                bot_response = generate_educational_response("Explain the 30% rule for rent", all_questions)
                st.session_state.chat_history.append({"role": "bot", "content": bot_response})
                st.rerun()
        
        with col2:
            if st.button("What is APR?"):
                st.session_state.chat_history.append({"role": "user", "content": "What is APR?"})
                bot_response = generate_educational_response("What is APR?", all_questions)
                st.session_state.chat_history.append({"role": "bot", "content": bot_response})
                st.rerun()
        
        with col3:
            if st.button("Stock Investing Basics"):
                st.session_state.chat_history.append({"role": "user", "content": "Explain stock investing basics"})
                bot_response = generate_educational_response("Explain stock investing basics", all_questions)
                st.session_state.chat_history.append({"role": "bot", "content": bot_response})
                st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Reset quiz button
        if st.button("Take Quiz Again"):
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.session_state.user_name = ""
            st.session_state.chat_history = []
            st.session_state.all_questions = []
            st.rerun()
