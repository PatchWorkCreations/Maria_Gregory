# How to Start the Django Server

## ⚠️ IMPORTANT: Always Activate Virtual Environment First!

The server **must** be started with the virtual environment activated, otherwise you'll get errors like:
```
ModuleNotFoundError: No module named 'cloudinary'
```

## ✅ Correct Way to Start the Server

### Option 1: Using PowerShell (Recommended)

1. Open PowerShell in the project root directory (`C:\Users\Tyagoooo\Downloads\Maria_Gregory`)

2. Activate the virtual environment:
   ```powershell
   .\myProject\venv\Scripts\Activate.ps1
   ```

3. Start the server:
   ```powershell
   python manage.py runserver
   ```

### Option 2: One-Line Command

Run this single command:
```powershell
.\myProject\venv\Scripts\Activate.ps1; python manage.py runserver
```

### Option 3: Using Command Prompt (cmd)

1. Open Command Prompt in the project root directory

2. Activate the virtual environment:
   ```cmd
   myProject\venv\Scripts\activate.bat
   ```

3. Start the server:
   ```cmd
   python manage.py runserver
   ```

## 🔍 How to Verify It's Working

After starting, you should see:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Django version X.X.X, using settings 'myProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## ❌ Common Mistakes

1. **Starting server without activating venv** - This will cause module import errors
2. **Using system Python instead of venv Python** - Always activate the virtual environment first
3. **Running from wrong directory** - Make sure you're in the project root where `manage.py` is located

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

**Note:** The virtual environment contains all the required packages including `cloudinary`, `django`, etc. Without it activated, Python can't find these packages!

