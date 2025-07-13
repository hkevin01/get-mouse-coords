# UI/UX Design Principles Guide

## Overview

This document outlines key design principles and Laws of UX that should be followed when building user interfaces. These principles help create interfaces that are not only beautiful but also intuitive and enjoyable to use.

**Reference**: [Laws of UX](https://lawsofux.com/) - A comprehensive collection of design principles backed by psychology and research.

## Core Design Laws & Application

### 📐 **Aesthetic-Usability Effect**
**Principle**: Users often perceive aesthetically pleasing design as design that's more usable.

**Apply by:**
- Clean, consistent spacing (proper margins and padding)
- Typography hierarchy (clear headings, readable fonts)
- Visual cues like subtle shadows or border separators
- Consistent color scheme and visual rhythm

### ⚡ **Hick's Law**
**Principle**: The time it takes to make a decision increases with the number and complexity of choices.

**Apply by:**
- Reduce visible options per screen
- Collapse complex settings into expandable sections
- Use progressive disclosure (show basic options first)
- Group related options together

### 🔄 **Jakob's Law**
**Principle**: Users spend most of their time on other sites/apps, so they prefer your interface to work the same way.

**Apply by:**
- Follow familiar UI patterns (standard button placement, navigation)
- Use conventional icons and interactions
- Match platform-specific conventions (Windows, macOS, Linux)
- Maintain consistency with similar applications

### 🎯 **Fitts's Law**
**Principle**: The time to acquire a target is a function of the distance to and size of the target.

**Apply by:**
- Make important buttons large and easily clickable
- Place frequently used controls within easy reach
- Avoid tiny click targets (minimum 44px for touch)
- Position related controls close together

### 📦 **Law of Proximity**
**Principle**: Objects that are near, or proximate to each other, tend to be grouped together.

**Apply by:**
- Group related controls using visual spacing
- Use containers (panels, cards) to organize content
- Bundle related inputs visually
- Separate unrelated elements with whitespace

### 🔄 **Zeigarnik Effect**
**Principle**: People remember interrupted or incomplete tasks better than completed ones.

**Apply by:**
- Show progress indicators in multi-step processes
- Provide save state feedback ("Saving..." notifications)
- Use breadcrumbs for navigation context
- Indicate unsaved changes clearly

### 📈 **Goal-Gradient Effect**
**Principle**: The tendency to approach a goal increases with proximity to the goal.

**Apply by:**
- Emphasize progress in workflows (progress bars, step indicators)
- Highlight the next action in a sequence
- Use primary button styling for main actions
- Show completion percentages

### 🎨 **Law of Similarity**
**Principle**: Elements that share visual characteristics are perceived as more related than elements that don't.

**Apply by:**
- Use consistent styles for similar elements (buttons, toggles, inputs)
- Maintain consistent icon sizing and spacing
- Apply uniform color coding for similar functions
- Keep typography consistent across similar content

### 🧠 **Miller's Law**
**Principle**: The average person can only keep 7 (±2) items in their working memory.

**Apply by:**
- Limit options to 5-9 items per group
- Chunk information into logical groups
- Use progressive disclosure for complex forms
- Default to collapsed sections for advanced options

### ⏱️ **Doherty Threshold**
**Principle**: Productivity soars when a computer and its users interact at a pace (<400ms) that ensures neither has to wait on the other.

**Apply by:**
- Aim for sub-400ms response times
- Use loading states for longer operations
- Implement optimistic UI updates
- Show skeleton screens or shimmer effects during loading

## Implementation Guidelines for PyQt Applications

### Visual Hierarchy
```python
# Typography Scale
FONT_SIZES = {
    'heading_large': 24,
    'heading_medium': 18,
    'heading_small': 14,
    'body': 12,
    'caption': 10
}

# Spacing Scale (pixels)
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32
}
```

### Color Palette
```python
COLORS = {
    'primary': '#2196F3',      # Blue
    'secondary': '#4CAF50',    # Green
    'danger': '#f44336',       # Red
    'warning': '#FF9800',      # Orange
    'background': '#FAFAFA',   # Light Gray
    'surface': '#FFFFFF',      # White
    'text_primary': '#212121', # Dark Gray
    'text_secondary': '#757575' # Medium Gray
}
```

### Button Guidelines
```python
# Minimum button sizes
MIN_BUTTON_HEIGHT = 36  # pixels
MIN_BUTTON_WIDTH = 80   # pixels

# Button hierarchy
PRIMARY_BUTTON = "background-color: #2196F3; color: white; font-weight: bold;"
SECONDARY_BUTTON = "background-color: transparent; border: 2px solid #2196F3; color: #2196F3;"
DANGER_BUTTON = "background-color: #f44336; color: white; font-weight: bold;"
```

### Layout Principles

#### Consistent Spacing
- Use multiples of 8px for spacing (8, 16, 24, 32)
- Maintain consistent margins and padding
- Group related elements with closer spacing

#### Visual Grouping
- Use containers (QGroupBox, QFrame) to group related controls
- Apply consistent styling to similar elements
- Use whitespace to separate different functional areas

#### Responsive Design
- Set minimum and maximum sizes for components
- Use proper layout managers (QVBoxLayout, QHBoxLayout, QGridLayout)
- Ensure text remains readable at different sizes

## Checklist for UI Review

### ✅ Aesthetic-Usability
- [ ] Consistent spacing throughout the interface
- [ ] Clear typography hierarchy
- [ ] Subtle visual cues (shadows, borders) enhance usability
- [ ] Color scheme is consistent and purposeful

### ✅ Simplicity (Hick's Law)
- [ ] Complex options are hidden in expandable sections
- [ ] No more than 7±2 primary options visible at once
- [ ] Progressive disclosure is used for advanced features

### ✅ Familiarity (Jakob's Law)
- [ ] Standard button placement and styling
- [ ] Conventional icons and interactions
- [ ] Consistent with platform guidelines

### ✅ Accessibility (Fitts's Law)
- [ ] Important buttons are large and easily clickable
- [ ] Frequently used controls are prominently placed
- [ ] Related controls are positioned close together

### ✅ Organization (Law of Proximity)
- [ ] Related elements are visually grouped
- [ ] Unrelated elements are separated with whitespace
- [ ] Logical information hierarchy is maintained

### ✅ Feedback (Zeigarnik Effect)
- [ ] Progress indicators for multi-step processes
- [ ] Clear save/loading states
- [ ] Unsaved changes are indicated

### ✅ Progression (Goal-Gradient Effect)
- [ ] Next steps are clearly highlighted
- [ ] Progress is visually represented
- [ ] Primary actions use prominent styling

### ✅ Consistency (Law of Similarity)
- [ ] Similar elements have similar styling
- [ ] Icon sizing and spacing is uniform
- [ ] Color coding is consistent

### ✅ Cognitive Load (Miller's Law)
- [ ] Information is chunked into logical groups
- [ ] Advanced options are collapsed by default
- [ ] No more than 7±2 items in any single group

### ✅ Performance (Doherty Threshold)
- [ ] UI responses are under 400ms when possible
- [ ] Loading states are shown for longer operations
- [ ] Optimistic UI updates are used where appropriate

## Resources

- [Laws of UX](https://lawsofux.com/) - Complete reference
- [Material Design Guidelines](https://material.io/design) - Google's design system
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) - Apple's design principles
- [Qt Style Sheets Reference](https://doc.qt.io/qt-5/stylesheet-reference.html) - PyQt styling documentation

## Notes

This guide is adapted from general web/mobile UX principles for desktop PyQt applications. While some concepts (like touch targets) may not directly apply, the underlying psychological principles remain relevant for creating intuitive desktop interfaces.

The key is to consistently apply these principles throughout the application to create a cohesive, professional, and user-friendly experience.
