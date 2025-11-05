#!/usr/bin/env python3
"""
Kids Schedule Notifier
Sends daily schedule for Marta and Arkasha via Telegram
"""

import asyncio
import aiohttp
from datetime import datetime
import locale
import random

# Устанавливаем русскую локаль для дней недели
try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
    except:
        pass

class KidsScheduleNotifier:
    def __init__(self):
        # Telegram settings
        self.telegram_token = "8442392037:AAEiM_b4QfdFLqbmmc1PXNvA99yxmFVLEp8"
        self.chat_id = "350766421"
        
        # Schedule data
        self.schedule = {
            'понедельник': [
                {'child': '👧 Марта', 'activity': '🇬🇧 Английский', 'time': '16:00-17:00'},
                {'child': '👦 Аркаша', 'activity': '📐 Математика', 'time': '19:00-20:00'}
            ],
            'вторник': [
                {'child': '👧 Марта', 'activity': '💃 Танцы', 'time': '17:30-19:00'},
                {'child': '👦 Аркаша', 'activity': '⚽ Футбол', 'time': '17:00-18:00'}
            ],
            'среда': [
                {'child': '👧 Марта', 'activity': '🤺 Фехтование', 'time': '15:00-16:30'},
                {'child': '👧 Марта', 'activity': '🇬🇧 Английский', 'time': '17:00-18:00'}
            ],
            'четверг': [
                {'child': '👧 Марта', 'activity': '💃 Танцы', 'time': '17:30-19:00'},
                {'child': '👦 Аркаша', 'activity': '⚽ Футбол', 'time': '17:00-18:00'}
            ],
            'пятница': [
                {'child': '👧 Марта', 'activity': '🤺 Фехтование', 'time': '15:00-16:30'},
                {'child': '👦 Аркаша', 'activity': '📐 Математика', 'time': '19:00-20:00'}
            ],
            'суббота': [
                {'child': '👧 Марта', 'activity': '🤺 Фехтование', 'time': '15:00-17:00'}
            ],
            'воскресенье': [
                {'child': '👧 Марта', 'activity': '🤺 Фехтование', 'time': '12:00-14:00'}
            ]
        }
        
        # Parenting tips
        self.marta_tips = [
            "🎯 Эмоциональная безопасность: Покажи, что всегда за неё, слушай без лекций и разбирай ситуации вместе",
            "💬 Разговоры по душам: Слушай без осуждения, особенно как 'малый подросток' — это строит связь",
            "🌟 Самостоятельность с границами: Дай зону ответственности (карманные деньги, выбор одежды)",
            "🏆 Похвала и мотивация: Хвали за процесс ('ты старалась'), а не только результат",
            "🎨 Поддержка увлечений: Интересуйся танцами, книгами, рисованием — спрашивай мнение",
            "📚 Школьные успехи: Помогай найти свой стиль учёбы, фокусируйся на любознательности",
            "👫 Друзья и социум: Следи за окружением, но не запрещай — подружки для неё как вселенная",
            "⚡ Физическая активность: Поощряй спорт, движение, игры — мозг и тело связаны",
            "😊 Чувство юмора: Шутите вместе, создавайте семейные мемы — это укрепляет отношения"
        ]
        
        self.arkasha_tips = [
            "❤️ Сохранить доверие: В 13 лет подросток начинает отдаляться — будь героем, который понимает, а не судит",
            "💬 Открытое общение: Слушай активно, обсуждай по душам, особенно о чувствах и вызовах",
            "🛡️ Эмоциональная безопасность: Покажи, что всегда на его стороне, особенно в пубертате",
            "🎯 Самостоятельность с границами: Дай больше ответственности (бюджет, выбор хобби)",
            "🏅 Похвала и мотивация: Хвали за усилия и прогресс ('ты стараешься'), а не только за результаты",
            "🎮 Поддержка увлечений: Интересуйся играми, спортом, гаджетами — спрашивай мнение",
            "📖 Школьные успехи: Помогай развивать навыки учёбы, фокусируйся на мышлении и интересах",
            "👥 Друзья и социум: Следи за компанией, но не запрещай — обсуждай риски открыто",
            "⚽ Физическая активность: Поощряй спорт, движение, здоровое питание — это помогает с энергией"
        ]
    
    async def send_telegram_message(self, message: str):
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print("✅ Telegram message sent successfully")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Telegram API error: {error_text}")
                        return False
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
            return False
    
    def get_today_schedule(self):
        """Get today's schedule based on current day of week"""
        today = datetime.now()
        
        # Format date and day of week in Russian
        date_str = today.strftime("%d.%m.%Y")
        week_number = today.isocalendar()[1]
        
        try:
            day_of_week = today.strftime("%A").lower()
            day_of_week_ru = {
                'monday': 'понедельник',
                'tuesday': 'вторник',
                'wednesday': 'среда', 
                'thursday': 'четверг',
                'friday': 'пятница',
                'saturday': 'суббота',
                'sunday': 'воскресенье'
            }.get(day_of_week, day_of_week)
        except:
            # Fallback if locale doesn't work
            days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
            day_of_week_ru = days[today.weekday()]
        
        today_activities = self.schedule.get(day_of_week_ru, [])
        
        return date_str, day_of_week_ru, today_activities, week_number
    
    def format_schedule_message(self, date_str: str, day_of_week: str, activities: list, week_number: int):
        """Format the schedule message for Telegram"""
        # Capitalize day of week
        day_capitalized = day_of_week.capitalize()
        
        # Get random tips
        marta_tip = random.choice(self.marta_tips)
        arkasha_tip = random.choice(self.arkasha_tips)
        
        message = f"#Дети #Расписание {date_str} {day_capitalized} неделя {week_number}\n\n"
        message += f"📅 <b>Расписание на {date_str}</b>\n"
        message += f"🗓️ <b>{day_capitalized}</b>\n\n"
        
        if activities:
            message += "👨‍👩‍👧‍👦 <b>Сегодня у детей:</b>\n\n"
            
            for i, activity in enumerate(activities, 1):
                message += f"{i}. {activity['child']}\n"
                message += f"   {activity['activity']}\n"
                message += f"   🕐 {activity['time']}\n"
                
                if i < len(activities):
                    message += "\n"
        else:
            message += "🎉 <b>Сегодня выходной! Занятий нет.</b>"
        
        message += "\n\n💡 <b>Совет дня:</b>\n"
        message += f"👧 Для Марты: {marta_tip}\n"
        message += f"👦 Для Аркаши: {arkasha_tip}\n\n"
        message += "💫 Хорошего дня!"
        
        return message
    
    async def send_daily_schedule(self):
        """Send today's schedule to Telegram"""
        print("🕐 Preparing daily schedule...")
        
        date_str, day_of_week, activities, week_number = self.get_today_schedule()
        
        print(f"📅 Today: {date_str}, {day_of_week}, week {week_number}")
        print(f"📋 Activities: {len(activities)}")
        
        message = self.format_schedule_message(date_str, day_of_week, activities, week_number)
        
        # Print to console for debugging
        print("\n" + "="*50)
        print(message.replace('<b>', '').replace('</b>', ''))
        print("="*50)
        
        # Send to Telegram
        print("\n📱 Sending to Telegram...")
        success = await self.send_telegram_message(message)
        
        if success:
            print("✅ Daily schedule sent successfully!")
        else:
            print("❌ Failed to send daily schedule")
        
        return success

async def main():
    """Main execution function"""
    try:
        notifier = KidsScheduleNotifier()
        await notifier.send_daily_schedule()
    except Exception as e:
        print(f"❌ Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
