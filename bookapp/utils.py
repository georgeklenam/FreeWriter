def get_category_icon(category_name):
    """
    Returns appropriate Font Awesome icon for each category
    """
    icon_mapping = {
        'fiction': 'fas fa-magic',
        'business': 'fas fa-chart-line',
        'science': 'fas fa-flask',
        'technology': 'fas fa-microchip',
        'self-help': 'fas fa-heart',
        'philosophy': 'fas fa-brain',
        'history': 'fas fa-landmark',
        'biography': 'fas fa-user-tie',
        'autobiography': 'fas fa-user-edit',
        'romance': 'fas fa-heart',
        'mystery': 'fas fa-search',
        'thriller': 'fas fa-exclamation-triangle',
        'fantasy': 'fas fa-dragon',
        'sci-fi': 'fas fa-rocket',
        'horror': 'fas fa-ghost',
        'poetry': 'fas fa-feather-alt',
        'drama': 'fas fa-theater-masks',
        'comedy': 'fas fa-laugh',
        'adventure': 'fas fa-compass',
        'travel': 'fas fa-plane',
        'cooking': 'fas fa-utensils',
        'health': 'fas fa-heartbeat',
        'fitness': 'fas fa-dumbbell',
        'education': 'fas fa-graduation-cap',
        'reference': 'fas fa-book-open',
        'children': 'fas fa-baby',
        'young-adult': 'fas fa-star',
        'religion': 'fas fa-pray',
        'spirituality': 'fas fa-om',
        'psychology': 'fas fa-brain',
        'sociology': 'fas fa-users',
        'politics': 'fas fa-balance-scale',
        'economics': 'fas fa-coins',
        'finance': 'fas fa-chart-pie',
        'marketing': 'fas fa-bullhorn',
        'leadership': 'fas fa-crown',
        'management': 'fas fa-users-cog',
        'entrepreneurship': 'fas fa-lightbulb',
        'investing': 'fas fa-chart-bar',
        'real-estate': 'fas fa-home',
        'law': 'fas fa-gavel',
        'medicine': 'fas fa-stethoscope',
        'engineering': 'fas fa-cogs',
        'mathematics': 'fas fa-square-root-alt',
        'physics': 'fas fa-atom',
        'chemistry': 'fas fa-vial',
        'biology': 'fas fa-dna',
        'astronomy': 'fas fa-telescope',
        'geology': 'fas fa-mountain',
        'environmental': 'fas fa-leaf',
        'art': 'fas fa-palette',
        'music': 'fas fa-music',
        'photography': 'fas fa-camera',
        'design': 'fas fa-paint-brush',
        'architecture': 'fas fa-building',
        'fashion': 'fas fa-tshirt',
        'sports': 'fas fa-trophy',
        'gaming': 'fas fa-gamepad',
        'comics': 'fas fa-comment-dots',
        'manga': 'fas fa-comment-dots',
        'graphic-novels': 'fas fa-comment-dots',
    }
    
    # Convert to lowercase and remove special characters for matching
    clean_name = category_name.lower().replace('-', ' ').replace('_', ' ')
    
    # Try exact match first
    if clean_name in icon_mapping:
        return icon_mapping[clean_name]
    
    # Try partial matches
    for key, icon in icon_mapping.items():
        if key in clean_name or clean_name in key:
            return icon
    
    # Default icon
    return 'fas fa-book'
