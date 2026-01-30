import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.patches import Rectangle, Circle, Wedge

# Page configuration
st.set_page_config(
    page_title="Happy Birthday Card",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS styling - applied directly to Streamlit containers with animations
st.markdown("""
<style>
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Apply background to main app container - FIXES WHITE GAPS */
    .stApp, .block-container, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 100vh;
    }
    
    /* Remove all padding from inner containers */
    .stApp > div, .block-container > div, [data-testid="stAppViewContainer"] > div {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Make plot container taller */
    .st-emotion-cache-1kyxreq {
        display: flex;
        justify-content: center;
        min-height: 80vh;
    }
    
    /* Celebration page background override */
    .celebration-bg {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important;
        min-height: 100vh;
    }
    
    /* Text styling for celebration page */
    .celebration-title {
        color: #ff4757;
        font-size: 48px;
        font-weight: 900;
        margin: 20px 0;
        line-height: 1.2;
        text-align: center;
    }
    
    .celebration-date {
        color: #4834d4;
        font-size: 28px;
        font-weight: 700;
        margin: 20px 0 30px 0;
        text-align: center;
    }
    
    .celebration-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        margin: 30px auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 5px solid gold;
        max-width: 600px;
    }
    
    .celebration-message {
        color: #2c3e50;
        font-size: 24px;
        font-weight: 700;
        margin: 20px 0;
        line-height: 1.3;
        text-align: center;
    }
    
    .celebration-quote {
        color: #7f8c8d;
        font-size: 22px;
        font-style: italic;
        margin: 25px 0;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        border-left: 4px solid #ff9a9e;
        line-height: 1.5;
        text-align: center;
    }
    
    .celebration-wish {
        color: #e84393;
        font-size: 26px;
        font-weight: 700;
        margin: 20px 0;
        line-height: 1.3;
        text-align: center;
    }
    
    /* Remove all padding from plot container */
    [data-testid="stPyplotGlobal"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Emoji animations for celebration page */
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.2);
        }
    }
    
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes shake {
        0%, 100% {
            transform: translateX(0);
        }
        25% {
            transform: translateX(-5px);
        }
        75% {
            transform: translateX(5px);
        }
    }
    
    /* Individual emoji animations */
    .emoji-float {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        font-size: 60px;
        margin: 0 10px;
    }
    
    .emoji-bounce {
        display: inline-block;
        animation: bounce 2s ease-in-out infinite;
        font-size: 60px;
        margin: 0 10px;
    }
    
    .emoji-spin {
        display: inline-block;
        animation: spin 4s linear infinite;
        font-size: 60px;
        margin: 0 10px;
    }
    
    .emoji-pulse {
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
        font-size: 60px;
        margin: 0 10px;
    }
    
    .emoji-shake {
        display: inline-block;
        animation: shake 0.5s ease-in-out infinite;
        font-size: 60px;
        margin: 0 10px;
    }
    
    .emoji-container {
        text-align: center;
        margin: 30px 0;
    }
    
    /* Animated icons */
    .icon-float {
        display: inline-block;
        animation: float 4s ease-in-out infinite;
        font-size: 40px;
        margin: 0 8px;
    }
    
    .icon-spin {
        display: inline-block;
        animation: spin 6s linear infinite;
        font-size: 40px;
        margin: 0 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'show_celebration' not in st.session_state:
    st.session_state.show_celebration = False

if 'animation_complete' not in st.session_state:
    st.session_state.animation_complete = False

if 'animation_stage' not in st.session_state:
    st.session_state.animation_stage = 0

# Drawing settings - TALLER canvas with more space at the top
# Made Y_LIMITS taller to start drawing lower from the top
X_LIMITS = (-120, 120)
Y_LIMITS = (-120, 140)  # Changed from (-100, 120) to (-120, 140) - TALLER canvas
FONT_SCALE = 1.0

# Vertical offset to move entire cake down (more offset for taller canvas)
CAKE_VERTICAL_OFFSET = -30  # Increased from -20 to -30 to move cake further down

def create_cake_figure():
    """Create a new matplotlib figure with TALLER aspect ratio."""
    fig, ax = plt.subplots(figsize=(12, 8))  # Increased height from 7 to 8
    ax.set_xlim(X_LIMITS)
    ax.set_ylim(Y_LIMITS)
    ax.axis('off')
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax

def apply_vertical_offset(y):
    """Apply vertical offset to move elements down."""
    return y + CAKE_VERTICAL_OFFSET

def draw_cake_stage(ax, stage):
    """
    Draw the cake to the specified animation stage.
    Returns True if drawing was performed, False otherwise.
    """
    # Clear the axis for each stage
    ax.clear()
    ax.set_xlim(X_LIMITS)
    ax.set_ylim(Y_LIMITS)
    ax.axis('off')
    
    # Stage 0: Initial empty plot
    if stage == 0:
        return True
    
    # Stage 1: Birthday message - STARTING LOWER FROM THE TOP
    if stage >= 1:
        # Positioned lower to start from further down
        ax.text(0, apply_vertical_offset(100), "Happy Birthday!",
                ha='center', fontsize=28,
                fontweight='bold', color='#ff6b6b', style='italic')
        ax.text(0, apply_vertical_offset(80), "January 31, 2026",
                ha='center', fontsize=20,
                color='#9c88ff', fontweight='bold')
    
    # Stage 2: Cake plate - MOVED FURTHER DOWN
    if stage >= 2:
        plate_width = 140
        plate = Rectangle((-plate_width/2, apply_vertical_offset(-40)), plate_width, 8,
                         color='silver', ec='gray', lw=2, alpha=0.8)
        ax.add_patch(plate)
    
    # Stage 3-5: Cake layers - MOVED FURTHER DOWN
    if stage >= 3:
        cake_width = 120
        cake_base = Rectangle((-cake_width/2, apply_vertical_offset(-32)), cake_width, 30,
                             color='#ffd166', ec='#e6ac00', lw=2)
        ax.add_patch(cake_base)
    
    if stage >= 4:
        middle_width = 100
        cake_middle = Rectangle((-middle_width/2, apply_vertical_offset(-2)), middle_width, 22,
                               color='#ff9a76', ec='#ff7b4a', lw=2)
        ax.add_patch(cake_middle)
    
    if stage >= 5:
        top_width = 80
        cake_top = Rectangle((-top_width/2, apply_vertical_offset(20)), top_width, 18,
                            color='#ff6b6b', ec='#ff4757', lw=2)
        ax.add_patch(cake_top)
    
    # Stage 6: Purple icing - MOVED FURTHER DOWN
    if stage >= 6:
        cake_width = 120
        middle_width = 100
        top_width = 80
        icing_positions = [
            ((-cake_width/2 + 5, apply_vertical_offset(-5)), cake_width - 10, 4),
            ((-middle_width/2 + 5, apply_vertical_offset(18)), middle_width - 10, 4),
            ((-top_width/2 + 5, apply_vertical_offset(36)), top_width - 10, 4)
        ]
        for (x, y), width, height in icing_positions:
            icing = Rectangle((x, y), width, height, color='#9c88ff', ec='#8c7ae6', lw=1)
            ax.add_patch(icing)
    
    # Stage 7: Cake text - MOVED FURTHER DOWN
    if stage >= 7:
        ax.text(0, apply_vertical_offset(27), "HAPPY", ha='center', fontsize=12,
                fontweight='bold', color='#4834d4')
        ax.text(0, apply_vertical_offset(5), "BIRTHDAY", ha='center', fontsize=12,
                fontweight='bold', color='#4834d4')
        ax.text(0, apply_vertical_offset(-20), "JACKIELOU", ha='center', fontsize=12,
                fontweight='bold', color='#4834d4')
    
    # Stage 8: Candles (without flames) - MOVED FURTHER DOWN
    if stage >= 8:
        candle_colors = ['#ff6b6b', '#4ecdc4', '#ffd166', '#ff9a76']
        candle_positions = np.linspace(-30, 30, 4)
        
        for i, x in enumerate(candle_positions):
            candle = Rectangle((x - 2, apply_vertical_offset(40)), 4, 20,
                              color=candle_colors[i], ec='gray', lw=1)
            ax.add_patch(candle)
            
            candle_top = Rectangle((x - 3, apply_vertical_offset(60)), 6, 2,
                                  color='white', ec='lightgray', lw=1)
            ax.add_patch(candle_top)
    
    # Stage 9: Candle flames - MOVED FURTHER DOWN
    if stage >= 9:
        candle_positions = np.linspace(-30, 30, 4)
        for x in candle_positions:
            flame = Wedge((x, apply_vertical_offset(63)), 3, 30, 150,
                         color='#ffd700', ec='#ff9500', lw=1)
            ax.add_patch(flame)
    
    # Stage 10: Balloons - HIGHER WITH MORE SPACE
    if stage >= 10:
        balloon_colors = ['#ff6b6b', '#9c88ff', '#ffd166']
        # Position balloons even higher with taller canvas
        balloon_positions = [(-80, 90), (0, 100), (80, 85)]
        
        for (x, y), color in zip(balloon_positions, balloon_colors):
            balloon = Circle((x, y), 12, color=color, ec=color, alpha=0.8)
            ax.add_patch(balloon)
            ax.plot([x, x], [y-12, y-30], color='gray', lw=1, alpha=0.5)
    
    # Stage 11: Final message - MOVED FURTHER DOWN
    if stage >= 11:
        ax.text(0, apply_vertical_offset(-85), "Happy Birthday on January 31, 2026!",
                ha='center', fontsize=18, fontweight='bold', color='#ff6b6b')
    
    return True

def show_celebration_page():
    """Display the celebration page with animated emojis."""
    # Apply celebration background
    st.markdown("""
    <style>
        .stApp, .block-container, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Use columns for centering instead of custom divs
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Celebration emojis with different animations
        st.markdown("""
        <div class="emoji-container">
            <span class="emoji-float">🎉</span>
            <span class="emoji-bounce">🎂</span>
            <span class="emoji-spin">🎁</span>
            <span class="emoji-pulse">🎈</span>
            <span class="emoji-shake">🥳</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Title
        st.markdown('<h1 class="celebration-title">HAPPY BIRTHDAY!</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="celebration-date">January 31, 2026</h2>', unsafe_allow_html=True)
        
        # Wish box
        st.markdown('<div class="celebration-message">🎊 Your wish has been made! 🎊</div>', unsafe_allow_html=True)
        st.markdown('<div class="celebration-message">Happy Birthday Jackielou Trongcoso</div>', unsafe_allow_html=True)
        st.markdown('<div class="celebration-quote">"May your day be filled with joy, laughter, and love"</div>', unsafe_allow_html=True)
        st.markdown('<div class="celebration-wish">Wishing you all the happiness in the world!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Icons with animations
        st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <span class="icon-float">✨</span>
            <span class="icon-spin">🍰</span>
            <span class="icon-float">✨</span>
            <span class="icon-spin">🎊</span>
            <span class="icon-float">✨</span>
            <span class="icon-spin">🥂</span>
            <span class="icon-float">✨</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer message
        st.markdown('<div style="color: #636e72; font-size: 20px; line-height: 1.6; margin: 30px 0; text-align: center;">Another year wiser, another year brighter!<br>May all your dreams and aspirations come true.</div>', unsafe_allow_html=True)
        
        # Restart button - centered with columns
        restart_col1, restart_col2, restart_col3 = st.columns([1, 2, 1])
        with restart_col2:
            if st.button("✨ Make Another Wish! ✨",
                        type="primary",
                        use_container_width=True,
                        key="restart_button"):
                # Reset all states
                st.session_state.clear()
                st.session_state.show_celebration = False
                st.session_state.animation_complete = False
                st.session_state.animation_stage = 0
                st.rerun()

# Define animation stages with their status messages
ANIMATION_STAGES = [
    (0, "Starting..."),
    (1, "🎉 Creating Birthday Card..."),
    (2, "🎨 Drawing cake plate..."),
    (3, "🎨 Adding cake base..."),
    (4, "🎨 Adding middle layer..."),
    (5, "🎨 Adding top layer..."),
    (6, "🎨 Decorating with icing..."),
    (7, "✏️ Writing birthday message..."),
    (8, "🕯️ Adding candles..."),
    (9, "🔥 Lighting candles..."),
    (10, "🎈 Adding balloons..."),
    (11, "🎂 HAPPY BIRTHDAY! 🎂")
]

# Main app logic
if st.session_state.show_celebration:
    show_celebration_page()
else:
    # Main page - Cake Drawing
    
    # Use columns to center content instead of custom divs
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # Create placeholders
        animation_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Check if animation needs to run or show final frame
        if not st.session_state.animation_complete:
            # Run the animation
            for stage_num, status_msg in ANIMATION_STAGES:
                # Update status
                status_placeholder.info(status_msg)
                
                # Create and draw cake
                fig, ax = create_cake_figure()
                draw_cake_stage(ax, stage_num)
                
                # Display the plot
                animation_placeholder.pyplot(fig, use_container_width=True)
                
                # Close figure to prevent memory leaks
                plt.close(fig)
                
                # Pause between stages (except for the last one)
                if stage_num < len(ANIMATION_STAGES) - 1:
                    time.sleep(0.5)
            
            # Mark animation as complete
            st.session_state.animation_complete = True
            st.session_state.animation_stage = 11
            
            # Final status and effects
            status_placeholder.success("✨ Your birthday cake is ready! ✨")
            st.balloons()
            time.sleep(2)
            
        else:
            # Show the final completed cake without animation
            fig, ax = create_cake_figure()
            draw_cake_stage(ax, st.session_state.animation_stage)
            animation_placeholder.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
            # Show final status
            status_placeholder.success("✨ Your birthday cake is ready! ✨")
        
        # Divider
        st.markdown("---")
        
        # "Make a wish!" button - centered with columns
        button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
        with button_col2:
            if st.button("🎂 MAKE A WISH!",
                        type="primary",
                        use_container_width=True,
                        key="wish_button"):
                # Set flag to transition to celebration
                st.session_state.show_celebration = True
                
                # Celebration effects
                st.balloons()
                
                # Immediate rerun to show celebration page
                st.rerun()#code here
