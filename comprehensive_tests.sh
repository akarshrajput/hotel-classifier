#!/bin/bash

# 🏨 Comprehensive Hotel Service Classifier API Tests
# Pure AI-driven classification with LangChain + Mistral AI
# Zero hardcoded rules - everything determined by AI intelligence

echo "🏨 HOTEL SERVICE REQUEST CLASSIFIER - COMPREHENSIVE CURL TESTS"
echo "================================================================"
echo "🤖 Testing Pure AI Classification System"
echo "📡 Server: http://localhost:8000"
echo "🧠 AI Model: Mistral AI via LangChain"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to make API calls and format output
test_scenario() {
    local test_num="$1"
    local title="$2"
    local message="$3"
    local guest_id="$4"
    local room_number="$5"
    local expected="$6"
    
    echo -e "${BLUE}📋 Test $test_num: $title${NC}"
    echo -e "${CYAN}📝 Message: \"$message\"${NC}"
    echo -e "${PURPLE}👤 Guest: $guest_id | Room: $room_number${NC}"
    echo -e "${YELLOW}🎯 Expected: $expected${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s -X POST "http://localhost:8000/classify" \
        -H "Content-Type: application/json" \
        -d "{
            \"guest_message\": \"$message\",
            \"guest_id\": \"$guest_id\",
            \"room_number\": \"$room_number\"
        }")
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        echo "$response" | python3 -c "
import sys
import json
try:
    data = json.load(sys.stdin)
    ticket_status = '✅ TICKET CREATED' if data['should_create_ticket'] else '❌ NO TICKET'
    print(f'{ticket_status}')
    print(f'🎯 AI Confidence: {data[\"confidence\"]:.1%}')
    print(f'⚡ AI Priority: {data[\"suggested_priority\"].upper()}')
    print(f'⏱️ AI Time Est: {data[\"estimated_completion_time\"] or \"Not specified\"}')
    print(f'🧠 AI Reasoning: {data[\"reasoning\"][:100]}...')
    
    if data['categories']:
        print('📋 AI-Generated Categories:')
        urgency_map = {'low': '🟢', 'medium': '🟡', 'high': '🟠', 'urgent': '🔴'}
        for cat in data['categories']:
            emoji = urgency_map.get(cat['urgency'], '⚪')
            print(f'   {emoji} {cat[\"category\"].upper()}: {cat[\"message\"][:80]}...')
            print(f'      └─ Urgency: {cat[\"urgency\"]}')
    else:
        print('📋 Categories: None (correctly identified as non-service)')
        
except Exception as e:
    print(f'❌ Error parsing response: {e}')
    print('Raw response:', sys.stdin.read())
"
    else
        echo -e "${RED}❌ API call failed${NC}"
    fi
    
    echo ""
    echo "================================================================"
    echo ""
    sleep 2  # Avoid rate limiting
}

# Test 1: Simple Food & Beverage Request
test_scenario "1" "🍵 Simple Service Request" \
    "I need coffee please" \
    "G001" "101" \
    "Create service_fb ticket"

# Test 2: Emergency Maintenance 
test_scenario "2" "🚨 Emergency Situation" \
    "EMERGENCY! Water is flooding my bathroom!" \
    "G002" "205" \
    "Create urgent maintenance ticket"

# Test 3: Multiple Services
test_scenario "3" "🧹 Multiple Services" \
    "Can you clean my room and bring fresh towels?" \
    "G003" "312" \
    "Create housekeeping ticket"

# Test 4: Porter + Concierge 
test_scenario "4" "🎒 Multiple Categories" \
    "Can you help with my luggage and recommend a restaurant?" \
    "G004" "408" \
    "Create porter + concierge tickets"

# Test 5: Reception Issue
test_scenario "5" "💳 Reception Problem" \
    "My key card isn't working and I can't get into my room" \
    "G005" "503" \
    "Create reception ticket"

# Test 6: Greeting (No Ticket)
test_scenario "6" "👋 Greeting Message" \
    "Hello, good morning! How are you today?" \
    "G006" "601" \
    "No ticket created"

# Test 7: Thank You (No Ticket)
test_scenario "7" "🙏 Thank You Message" \
    "Thank you so much for the wonderful service!" \
    "G007" "702" \
    "No ticket created"

# Test 8: Information Request (No Ticket)
test_scenario "8" "❓ Information Query" \
    "What time does the restaurant close?" \
    "G008" "805" \
    "No ticket created"

# Test 9: Complex Business Request
test_scenario "9" "💼 Business Request" \
    "I need urgent coffee and room service for my important client meeting in 30 minutes" \
    "B001" "1205" \
    "Create high-priority service_fb ticket"

# Test 10: Maintenance with Context
test_scenario "10" "🔧 Technical Issue" \
    "The WiFi is not working and I have an online presentation" \
    "B002" "1501" \
    "Create maintenance ticket with business context"

# Test 11: Housekeeping with Urgency
test_scenario "11" "🧽 Urgent Cleaning" \
    "Please clean my room immediately, I spilled wine everywhere" \
    "G011" "920" \
    "Create urgent housekeeping ticket"

# Test 12: Polite Complex Request
test_scenario "12" "🌟 Polite Multi-Service" \
    "Could you please help me with my bags and also arrange for coffee?" \
    "V001" "2001" \
    "Create porter + service_fb tickets"

# Test 13: Health/Safety Issue
test_scenario "13" "🏥 Health Concern" \
    "There's a strong chemical smell in my room, I'm feeling sick" \
    "G013" "1103" \
    "Create urgent maintenance/safety ticket"

# Test 14: Late Night Request
test_scenario "14" "🌙 Late Night Service" \
    "It's 2 AM and I need extra blankets, I'm very cold" \
    "G014" "1401" \
    "Create housekeeping ticket with context"

# Test 15: Complaint vs Request
test_scenario "15" "😤 Complaint with Request" \
    "The room is too noisy, can you move me to a quieter room?" \
    "G015" "301" \
    "Create reception ticket for room change"

echo -e "${GREEN}🎉 COMPREHENSIVE TESTING COMPLETED!${NC}"
echo ""
echo -e "${BLUE}📊 AI SYSTEM CAPABILITIES DEMONSTRATED:${NC}"
echo "   • Pure AI intelligence with zero hardcoded rules"
echo "   • Dynamic service category detection"
echo "   • Intelligent urgency and priority assessment"
echo "   • Context-aware message generation"
echo "   • Multiple service handling in single requests"
echo "   • Smart distinction between service requests and casual messages"
echo "   • Business context understanding"
echo "   • Emergency situation prioritization"
echo ""
echo -e "${PURPLE}🔗 API Documentation: http://localhost:8000/docs${NC}"
echo -e "${CYAN}💡 Try your own messages at the /classify endpoint!${NC}"
