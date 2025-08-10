# LanguaTale

## Project Overview

LanguaTale is a story-based language learning web application. It allows users to learn languages through stories.

*Note: A basic understanding of the target language is needed to utilise the app fully.*

## How to Run

1. Open terminal and navigate to the project directory:

   *Note: You need to cd into languatale twice due to the project folder structure.*

   ```bash
   cd LanguaTale/languatale/languatale

2. Start Django development server
   ```bash
   python manage.py runserver

## AI Usage Report

### MANUALLY WRITTEN (No AI Assistance)
| File                         | Lines   | Description                   | Notes                                 |
|------------------------------|---------|-------------------------------|--------------------------------------|
| account.html                 | 1-71    | User account page             | Manual HTML setup with external sources (Google Fonts, SVG icons) |
| completed_stories.html       | 1-66    | Stories completion page       |                                      |
| home.html                   | 1-68    | Main homepage layout          |                                      |
| login.html                  | 1-36    | Login form page structure     |                                      |
| play_story.html             | 1-73    | Interactive story page layout |                                      |
| signup.html                 | 1-114   | User registration form        |                                      |
| welcome.html                | 1-29    | Welcome page layout           |                                      |
| models.py                  | 1-33    | Database models setup         |                                      |
| admin.py                   | 1-24    | Admin interface setup         | Manual Django admin setup            |
| urls.py                    | 1-25    | URL routing                   |                                      |
| forms.py                   | 1-22    | Form logic                   | Custom Form setup                    |
| password_reset_*.html      | Various | Custom templates              |                                      |

### PARTIALLY AI-ASSISTED
| File                  | Lines  | AI Contribution          | Manual Contribution                   |
|-----------------------|--------|-------------------------|-------------------------------------|
| account.css           | 17-187 | Styling suggestions     | Custom layout, color choices        |
| completed_stories.css | 1-37   | Layout enhancements     | Grid layout and basic styling       |
| home.css              | 1-171  | Advanced CSS properties | Page layout and color choices       |
| play_story.css        | 1-278  | Interactive elements    | Base styling and positioning        |
| signup.css            | 1-99   | Form validation styling | Layout and custom design             |
| welcome.css           | 1-88   | Interface styling       | Basic structure and positioning     |
| views.py              | 69-133 | Complex view functions  | Simple view functions                |

### AI GENERATED (Significant AI Assistance)
| File               | Lines   | Description                   | Learning Outcome                     |
|--------------------|---------|-------------------------------|------------------------------------|
| play_story.js       | 51-308  | Interactive story logic        | JS functions, events, JSON handling & gTTS |
