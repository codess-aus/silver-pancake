# Usage Guide - Silver Pancake AI Meme Generator

## 🚀 Getting Started

### For End Users

#### 1. Access the Application
- Open your browser to the Silver Pancake URL
- You'll see a clean, modern interface with a meme generation form

#### 2. Generate Your First Meme
1. **Enter a Topic**: Type any workplace or general topic (e.g., "coffee breaks", "debugging", "Monday meetings")
2. **Choose a Mood**: Select from funny, sarcastic, wholesome, motivational, or relatable
3. **Click "Generate Meme"**: Wait a few seconds for AI generation and safety analysis
4. **View Results**: See your meme text in both creative and classic formats

#### 3. Safety Features
- ✅ **Green Badge**: Indicates content passed all safety checks
- ⚠️ **Safety Notice**: If content is blocked, try a different topic or mood
- 🚩 **Flag Button**: Report any inappropriate content that got through

### For Developers

#### 1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/codess-aus/silver-pancake.git
cd silver-pancake

# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your Azure credentials
uvicorn main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm start
```

#### 2. API Usage

**Generate Meme Endpoint**:
```http
POST /api/generate-meme
Content-Type: application/json

{
  "topic": "work from home",
  "mood": "funny"
}
```

**Response**:
```json
{
  "success": true,
  "meme_text": "When you're working from home...",
  "top_text": "WHEN YOU'RE ON A VIDEO CALL",
  "bottom_text": "BUT YOUR CAT BECOMES THE CEO",
  "topic": "work from home",
  "mood": "funny",
  "is_safe": true,
  "message": "Meme generated successfully!"
}
```

**Feedback Endpoint**:
```http
POST /api/feedback
Content-Type: application/json

{
  "meme_text": "Problematic content here",
  "reason": "inappropriate",
  "user_comment": "This doesn't seem workplace appropriate"
}
```

#### 3. Configuration Options

**Environment Variables**:
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI resource endpoint
- `AZURE_OPENAI_API_KEY`: API key for OpenAI access
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Deployed model name (e.g., "gpt-4")
- `AZURE_CONTENT_SAFETY_ENDPOINT`: Content Safety resource endpoint
- `AZURE_CONTENT_SAFETY_API_KEY`: Content Safety API key
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)

**Safety Thresholds** (in `backend/services/content_safety_service.py`):
```python
SEVERITY_THRESHOLD = 2  # Adjust based on your risk tolerance
```

## 🎯 Best Practices

### For Users

#### Creating Great Memes
- **Be Specific**: "Daily standup meetings" works better than just "meetings"
- **Try Different Moods**: The same topic can be funny, motivational, or relatable
- **Keep It Professional**: Focus on universal workplace experiences
- **Iterate**: If the first result isn't perfect, try rephrasing your topic

#### Content Guidelines
✅ **Great Topics**:
- "Code reviews"
- "Coffee machine broken"
- "Project deadlines"
- "Team building activities"
- "Remote work challenges"

❌ **Avoid**:
- Personal information or names
- Controversial political topics
- Sensitive company information
- Discriminatory content

### For Developers

#### Extending the Application

**Add New Moods**:
1. Update the `moodOptions` array in `frontend/src/components/MemeGenerator.js`
2. Modify the system prompt in `backend/services/openai_service.py` to handle new moods
3. Test thoroughly with safety evaluation

**Customize Safety Thresholds**:
1. Adjust `SEVERITY_THRESHOLD` in `ContentSafetyService`
2. Run comprehensive safety evaluation: `python evaluations/run_evaluation.py --type safety`
3. Monitor false positive/negative rates

**Add New Features**:
1. Create new API endpoints in `backend/main.py`
2. Add corresponding frontend components
3. Include in automated test suite
4. Update documentation

#### Performance Optimization

**Caching Strategies**:
- Cache popular topic/mood combinations
- Implement Redis for session management
- Use CDN for static frontend assets

**Monitoring**:
- Enable Azure Application Insights
- Monitor API response times and error rates
- Set up alerts for safety system failures

## 🔧 Troubleshooting

### Common Issues

#### "Failed to generate meme"
- **Check Azure Credentials**: Verify API keys and endpoints in `.env`
- **Verify Deployments**: Ensure GPT-4 model is deployed and active
- **Check Quotas**: Verify you haven't exceeded Azure usage limits

#### Content Constantly Blocked
- **Review Topics**: Try more general, workplace-appropriate topics
- **Adjust Thresholds**: Consider slightly raising safety thresholds (with caution)
- **Check Logs**: Review backend logs for specific safety failures

#### Frontend Not Connecting to Backend
- **CORS Settings**: Verify `CORS_ORIGINS` includes your frontend URL
- **Proxy Configuration**: Check `proxy` setting in `frontend/package.json`
- **Network Issues**: Ensure both frontend and backend are running

### Debugging Steps

1. **Check Logs**: Backend logs show detailed error information
2. **Test Endpoints**: Use `/health` endpoint to verify backend is running
3. **API Documentation**: Visit `/docs` for interactive API testing
4. **Run Evaluations**: Use evaluation scripts to test system health

### Getting Help

- **Documentation**: Check `/docs` folder for detailed guides
- **GitHub Issues**: Report bugs with detailed reproduction steps
- **Discussions**: Ask questions in GitHub Discussions
- **Logs**: Include relevant log output when reporting issues

## 📊 Monitoring and Analytics

### User Analytics
- Track popular topics and moods
- Monitor user satisfaction through feedback
- Analyze content safety patterns

### System Health
- API response times and success rates
- Safety system accuracy and performance
- Error rates and common failure modes

### Safety Metrics
- Content flagging rates by category
- False positive/negative analysis
- User feedback correlation with safety scores

## 🚀 Advanced Usage

### Batch Processing
For generating multiple memes programmatically:

```python
import asyncio
import aiohttp

async def generate_memes_batch(topics_and_moods):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for topic, mood in topics_and_moods:
            task = generate_single_meme(session, topic, mood)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

### Custom Integration
Integrate with workplace tools:

```javascript
// Slack bot integration example
app.post('/slack/meme', async (req, res) => {
    const { topic, mood } = parseSlackCommand(req.body.text);
    
    const meme = await generateMeme(topic, mood || 'funny');
    
    if (meme.is_safe) {
        res.json({
            response_type: 'in_channel',
            text: meme.meme_text
        });
    } else {
        res.json({
            response_type: 'ephemeral', 
            text: 'Sorry, that topic didn\'t generate appropriate content. Try something else!'
        });
    }
});
```

### Evaluation and Testing

Run comprehensive evaluations:

```bash
# Full evaluation with detailed reporting
python evaluations/run_evaluation.py --type full --output results/ --verbose

# Safety-focused evaluation
python evaluations/run_evaluation.py --type safety --verbose

# Custom test with specific topics
python -c "
import asyncio
from evaluations.run_evaluation import MemeEvaluator

async def custom_test():
    evaluator = MemeEvaluator('evaluation_config.json')
    result = await evaluator.run_safety_evaluation()
    print(f'Safety Score: {result[\"accuracy\"]:.2%}')

asyncio.run(custom_test())
"
```

---

## 🎉 Success Stories

### Typical Use Cases

**Team Building**: "Generate funny memes about our sprint retrospectives"
**Training**: "Create engaging content for new employee onboarding"  
**Communication**: "Add humor to internal newsletters and announcements"
**Morale**: "Lighten the mood during stressful project periods"

### Best Results

Users report the best results when:
- Being specific about workplace scenarios
- Trying multiple mood options for the same topic
- Using the feedback system to improve future generations
- Combining generated text with visual meme templates

Remember: Silver Pancake is designed to enhance team communication and morale while maintaining professional standards and safety. Have fun, be creative, and help us improve the system through your feedback!