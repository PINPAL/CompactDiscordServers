import json
import os
import re
import shutil
from bs4 import BeautifulSoup


def replace_patterns_in_file(file_path, pattern_to_replace, replacement_text):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        
        # log the number of matches
        matches = len(re.findall(pattern_to_replace, file_contents))
        print(f"Found {matches} matches for {replacement_text} replace.")
        file_contents = re.sub(pattern_to_replace, replacement_text, file_contents)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_contents)
        
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_junk_files(directory_name):
    if os.path.isdir(directory_name):
        for file_name in os.listdir(directory_name):
            if file_name.endswith('.webp') or file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.js'):
                file_path = os.path.join(directory_name, file_name)
                os.remove(file_path)
                print(f"Removed {file_path}")
    else:
        print(f"The directory {directory_name} does not exist.")
        
def findFullClassname(soup, classname):
    for tag in soup.find_all(class_=re.compile(classname)):
        return tag['class'][0]
    return None

def replaceHrefPath(soup, matchString, replacementString):
    for tag in soup.find_all(href=re.compile(matchString)):
        tag['href'] = replacementString

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Regex to be replaced
    games = r'(Overwatch® 2)|(Counter Strike 2)|(PUBG)'
    # Read the usernames/servers/groupchats from usernames.json file
    usernamesFile = os.path.join(current_directory, "usernames.json")
    usernamesFile = json.load(open(usernamesFile))
    # Construct the regex pattern to match all usernames
    usernames = r''
    for username in usernamesFile["usernames"]:
        usernames += rf'(?<!\w){re.escape(username)}(?!\w)|'
    usernames = usernames[:-1]  # Remove the last pipe character
    usernames = re.compile(rf'{usernames}', re.IGNORECASE)
    # Construct the regex pattern to match all groupchats
    groupchats = r''
    for groupchat in usernamesFile["groupchats"]:
        groupchats += rf'(?<!\w){re.escape(groupchat)}(?!\w)|'
    groupchats = groupchats[:-1]  # Remove the last pipe character
    # Construct the regex pattern to match all servers
    servers = r''
    for server in usernamesFile["servers"]:
        servers += rf'(?<!\w){re.escape(server)}(?!\w)|'
    servers = servers[:-1]  # Remove the last pipe character
    
    # Find all HTML files in the current directory
    dump_files_path = os.path.join(current_directory, "discord-dump")
    dumped_html_files = [f for f in os.listdir(dump_files_path) if f.endswith('.html')]
    if not dumped_html_files:
        print("No HTML files found in the current directory.")
        return
    
    # Delete the old index.html
    old_index_path = os.path.join(dump_files_path, "index.html")
    if os.path.exists(old_index_path):
        os.remove(old_index_path)
        print("Removed old index.html")
        
    # Get the name of the first HTML file
    html_file = dumped_html_files[0]
    print("Found file: " + html_file)
    html_file_path = os.path.join(dump_files_path, html_file)
    html_files_directory_name = html_file.rsplit('.html', 1)[0] + "_files"
    html_files_directory_path = os.path.join(dump_files_path, html_files_directory_name )
    
    # Create the target files 
    new_html_file_path = os.path.join(dump_files_path, "index.html")

    # Create a copy of the original HTML file as "index.html"
    if not os.path.exists(new_html_file_path):
        shutil.copy(html_file_path, new_html_file_path)
    
    # Remove <script>.*</script> from the new HTML file
    pattern = re.compile(r'<script\b[^>]*>([\s\S]*?)<\/script>', re.IGNORECASE)
    replace_patterns_in_file(new_html_file_path, pattern, '')
    
    # Construct a regex pattern to match all user images
    user_image_pattern = rf'src="\./{re.escape(html_files_directory_name)}/[^"]*\.(webp|png)"'
    user_image_pattern = rf'src="\./{re.escape(html_files_directory_name)}/[^"]*\.(webp|png)"'
    print(user_image_pattern)
    server_image_pattern = rf'class="icon_f90abb" src="\./\.\.\/generic-user\.png"'

    # Replace patterns in the new HTML file
    replace_patterns_in_file(new_html_file_path, usernames, "Username")
    replace_patterns_in_file(new_html_file_path, games, "Generic Game")
    replace_patterns_in_file(new_html_file_path, groupchats, "Group Name")
    replace_patterns_in_file(new_html_file_path, servers, "Server Name")
    replace_patterns_in_file(new_html_file_path, user_image_pattern, 'src="./../generic-user.png"')
    replace_patterns_in_file(new_html_file_path, server_image_pattern, 'class="icon__0cbed" src="./../generic-server.png"')
    
    # Remove all unused files from the original directory 
    remove_junk_files(html_files_directory_path)
    
    # Load the HTML content from the file
    with open(new_html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
    # Find the <html> tag and add the "app-focused" class to it (to emulate the Discord Client app being focused)
    html_tag = soup.find('html')
    if html_tag:
        if 'class' in html_tag.attrs:
            html_tag['class'].append('app-focused')  # Add to existing classes
        else:
            html_tag['class'] = ['app-focused']  # Add new class 
        
    # Find and remove the <div> with class 'drag-previewer'
    # This div is completely broken without the JavaScript that Discord uses
    for div in soup.find_all('div', class_='drag-previewer'):
        div.decompose()  # This removes the tag from the tree
        
    # Add the stylesheet link to the new HTML file
    link_tag = soup.new_tag('link')
    link_tag['rel'] = 'stylesheet'
    link_tag['href'] = './../../assets/css/main.css'
    soup.head.append(link_tag)
    
    # Add the theme selector to the new HTML file 
    # ===========================================
    # Get the theme.html file and add it to the new HTML file
    theme_path = os.path.join(current_directory, 'theme.html')
    with open(theme_path, 'r', encoding='utf-8') as file:
        theme_soup = BeautifulSoup(file, 'html.parser')
        theme_div = theme_soup.find('div', class_='themeEditor')
        theme_style = theme_soup.find('style', id='theme-style')
        div_to_add_to = soup.find('div', class_=findFullClassname(soup, 'appAsidePanelWrapper_'))
        div_to_add_to.append(theme_div)
        soup.head.append(theme_style)
    # Add the theme.js script to the new HTML file
    script_tag = soup.new_tag('script')
    script_tag['src'] = './../theme.js'
    soup.body.append(script_tag)
    # Add the theme.css link to the new HTML file
    theme_link_tag = soup.new_tag('link')
    theme_link_tag['rel'] = 'stylesheet'
    theme_link_tag['href'] = './../theme.css'
    soup.head.append(theme_link_tag)
    
    # Write the modified content back to the file
    with open(new_html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))
    

if __name__ == "__main__":
    main()
