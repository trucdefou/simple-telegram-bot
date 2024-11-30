
# Telegram Bot for Lists and Reminders  

## **About The Project**  
This bot helps you organize tasks and reminders directly within Telegram. It offers an easy-to-use interface with inline buttons for creating, viewing, and deleting reminders.   

---

### **Built With**  
- **Python**: Core programming language.  
- **python-telegram-bot**: Telegram API wrapper for bot functionality.  
- **JSON**: Used for storing and retrieving reminder data.   

---

## **Getting Started**  
Follow these steps to set up and run the bot locally.  

### **Prerequisites**  
Ensure you have Python 3.10 or later installed.  

### **Installation**  

1. Clone the repository:  
   ```sh  
   git clone https://github.com/trucdefou/telegram-reminder-bot.git  
   cd telegram-reminder-bot  
   ```  

2. Create a virtual environment:  
   ```sh  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```  

3. Install dependencies:  
   ```sh  
   pip install -r requirements.txt  
   ```  

4. Set your Telegram API Token:  
   - Create a `.env` file in the root directory.  
   - Add your token:  
     ```env  
     TELEGRAM_TOKEN=your_telegram_bot_token  
     ```  

5. Run the bot:  
   ```sh  
   python bot.py  
   ``` 

---

## **Usage**  
- **Add Reminder**: Create tasks and add them to your reminder list.  
- **View Reminders**: See all your saved reminders in a list.  
- **Delete Reminder**: Select and remove tasks using inline buttons.  
- **Cancel Actions**: Exit any action with a "Cancel" button.  

- **Add list**: Create tasks and add them to your reminder list.  
- **View list**: See all your saved reminders in a list.  
- **Delete list**: Select and remove tasks using inline buttons.  
- **Cancel Actions**: Exit any action with a "Cancel" button.  

---

1. Fork the repository.  
2. Create a new branch:  
   ```sh  
   git checkout -b feature/YourFeature  
   ```  
3. Commit your changes:  
   ```sh  
   git commit -m "Add YourFeature"  
   ```  
4. Push to the branch:  
   ```sh  
   git push origin feature/YourFeature  
   ```  
5. Open a pull request.  

---

## **License**  
Distributed under the MIT License. See `LICENSE` for more information.  


---

## **Contact**  
**Your Name**  
[lucianorecalde92@gmail.com](mailto:lucianorecalde92@gmail.com)  
[GitHub Profile](https://github.com/trucdefou)  


---

## **Acknowledgments**  
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)  
- [Telegram Bot API](https://core.telegram.org/bots/api)   

