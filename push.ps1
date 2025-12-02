# Quick Push Script
# After creating the GitHub repo, replace YOUR_USERNAME and run this

# Set your GitHub username here
$GITHUB_USERNAME = "YOUR_USERNAME"  # <-- CHANGE THIS

# Add remote
git remote add origin "https://github.com/$GITHUB_USERNAME/medical-rag-chatbot.git"

# Rename branch to main
git branch -M main

# Push everything (including LFS files)
Write-Host "Pushing to GitHub... This will take 5-10 minutes (uploading 1.6GB)" -ForegroundColor Yellow
git push -u origin main

Write-Host "`n✅ Push complete! Check: https://github.com/$GITHUB_USERNAME/medical-rag-chatbot" -ForegroundColor Green
