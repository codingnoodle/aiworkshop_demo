# 🚀 GitHub Codespaces Setup Guide

This guide helps you set up this repository on GitHub Codespaces for your workshop audience.

## 📋 Prerequisites

- GitHub account
- Repository created on GitHub
- Basic familiarity with GitHub

## 🔧 Setup Steps

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"** (green button)
3. **Repository name**: `clinical-trials-navigator` (or your preferred name)
4. **Description**: "AI-powered clinical trial search and analysis tool for workshop"
5. **Make it Public** (so participants can access it)
6. **Don't initialize** with README (we already have one)
7. **Click "Create repository"**

### Step 2: Push Your Code

```bash
# In your local project directory
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 3: Enable Codespaces

1. **Go to your repository** on GitHub
2. **Click the green "Code" button**
3. **Click "Codespaces" tab**
4. **Click "Create codespace on main"**
5. **Wait for setup** (2-3 minutes first time)

### Step 4: Test the Setup

1. **In the Codespace terminal**, run:
   ```bash
   streamlit run app.py
   ```
2. **Click the URL** that appears (usually `https://xxxx-8501.preview.app.github.dev`)
3. **Test the app** by entering "diabetes" in the chat box

## 🎓 Sharing with Workshop Participants

### Option 1: Direct Repository Link
Share this link with participants:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

### Option 2: Codespace Template Link
Create a template link:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/generate
```

### Option 3: Workshop Instructions
Create a simple instruction document:

```markdown
# Workshop Setup Instructions

1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for setup (2-3 minutes)
4. In the terminal, run: `streamlit run app.py`
5. Click the URL that appears
6. Start with: Enter "diabetes" in the chat box
7. Follow exercises in WORKSHOP_README.md
```

## 🔧 Codespace Configuration

The repository includes these Codespace optimizations:

### `.devcontainer/devcontainer.json`
- **Python 3.11** environment
- **Pre-installed extensions**: Python, Jupyter, Black formatter
- **Port forwarding**: Automatically forwards port 8501 for Streamlit
- **Post-create command**: Automatically installs dependencies

### Workshop Files
- **`WORKSHOP_README.md`**: Workshop-specific instructions
- **`setup_workshop.py`**: Automated setup script
- **`start_workshop.sh`**: One-click launch script

## 🎯 Workshop Flow

### For Participants (5 minutes total):
1. **Click repository link** → **Create Codespace** (2-3 min)
2. **Run**: `streamlit run app.py` (30 sec)
3. **Click URL** → **Start exploring** (1-2 min)

### For Instructors:
1. **Share repository link** with participants
2. **Guide through first exercise** (diabetes search)
3. **Let participants explore** with WORKSHOP_README.md
4. **Answer questions** as they arise

## 🚨 Troubleshooting

### Codespace won't start?
- Check GitHub account limits
- Try creating a new Codespace
- Ensure repository is public

### App won't run?
```bash
# In Codespace terminal
pip install -r requirements.txt
streamlit run app.py
```

### Port not forwarding?
- Check the "Ports" tab in VS Code
- Manually forward port 8501
- Look for the preview URL in terminal

### Dependencies missing?
```bash
# Reinstall everything
pip install --upgrade -r requirements.txt
```

## 💡 Pro Tips

### For Instructors:
- **Test beforehand**: Create your own Codespace to verify setup
- **Have backup plan**: Local installation instructions ready
- **Monitor progress**: Check if participants are stuck
- **Use breakout rooms**: For hands-on help

### For Participants:
- **Bookmark the URL**: Save the Streamlit app URL
- **Read WORKSHOP_README.md**: Contains all exercises
- **Ask questions**: Use chat or raise hand
- **Explore freely**: Try different medical conditions

## 📊 Workshop Timing

### 5-minute setup:
- Repository access and Codespace creation
- App launch and first test

### 15-minute exploration:
- Basic search exercises
- Profile setup and personalization
- Interactive features

### 10-minute discussion:
- Technical architecture
- Real-world applications
- Q&A session

## 🎉 Success Metrics

Workshop is successful when participants can:
- [ ] Create a Codespace from the repository
- [ ] Launch the Streamlit app
- [ ] Search for clinical trials
- [ ] Use interactive features (map, profiles)
- [ ] Understand the AI workflow
- [ ] Ask informed questions about the technology

## 📞 Support

### For Technical Issues:
- GitHub Codespaces documentation
- Streamlit documentation
- Repository issues page

### For Workshop Issues:
- Prepare backup local installation
- Have screenshots of key features
- Prepare demo data for offline use

---

**Ready to run your workshop? Share the repository link and let participants explore!** 🚀
