"""
Script to simplify plotly field descriptions using LLM calls.
Removes boilerplate while preserving essential information.
"""

import re
import json
from typing import List, Dict, Tuple
import os

# For production use with OpenAI:
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_field_info(line: str) -> Tuple[str, str, str]:
    """Extract field name, type, and description from a field line"""
    # Match pattern: field_name: Type = Field(default=..., description="...")
    match = re.match(r'(\s*)(\w+):\s*([^=]+)\s*=\s*Field\(([^)]+)\)', line)
    if match:
        indent = match.group(1)
        field_name = match.group(2)
        field_type = match.group(3).strip()
        field_args = match.group(4)
        
        # Extract description from field_args
        desc_match = re.search(r'description="([^"]*(?:\\.[^"]*)*)"', field_args)
        if desc_match:
            description = desc_match.group(1)
            return field_name, field_type, description, indent, field_args
    
    return "", "", "", "", ""

def simplify_descriptions_batch(descriptions: List[Dict]) -> List[str]:
    """Use LLM to simplify a batch of descriptions"""
    
    # Create the prompt for batch processing
    prompt = """You are helping to simplify verbose plotly parameter descriptions for better LLM understanding.

TASK: Simplify these field descriptions by:
1. Remove boilerplate like "Either a name of a column in `data_frame`, or a pandas Series or array_like object"
2. Keep the core functionality and purpose
3. Preserve important constraints, valid values, and behavior details
4. Make them concise but clear
5. Keep technical terms that are essential

INPUT FORMAT: Each description is numbered and contains the field name and current description.

OUTPUT FORMAT: Return ONLY the simplified descriptions in the same order, one per line, starting with the number.

EXAMPLES:
Input: "Either a name of a column in `data_frame`, or a pandas Series or array_like object. Values from this column are used to position marks along the x axis in cartesian coordinates."
Output: "Values used to position marks along the x-axis."

Input: "Strings should define valid CSS-colors. When `color` is set and the values in the corresponding column are not numeric, values in that column are assigned colors by cycling through `color_discrete_sequence` in the order described in `category_orders`."
Output: "CSS color strings. Colors are assigned by cycling through this sequence when `color` column is non-numeric."

Here are the descriptions to simplify:

"""
    
    # Add descriptions to prompt
    for i, desc_info in enumerate(descriptions, 1):
        prompt += f"{i}. {desc_info['field_name']}: {desc_info['description']}\n"
    
    # Use OpenAI API to simplify descriptions
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an expert at simplifying technical documentation while preserving essential information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        simplified = response.choices[0].message.content.strip().split('\n')
        return [line.split('. ', 1)[1] if '. ' in line else line for line in simplified]
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        print("Falling back to rule-based simplification...")
        # Fall back to rule-based approach if API fails
    
    # Mock simplified descriptions for demonstration
    simplified = []
    for desc_info in descriptions:
        desc = desc_info['description']
        field_name = desc_info['field_name']
        
        # Apply some basic simplification rules as examples
        simplified_desc = desc
        
        # Remove common boilerplate
        simplified_desc = re.sub(r'Either a name of a column in `data_frame`, or a pandas Series or array_like object\. ', '', simplified_desc)
        simplified_desc = re.sub(r'Values from this column or array_like are used to ', 'Used to ', simplified_desc)
        simplified_desc = re.sub(r'This argument needs to be passed for column names \(and not keyword names\) to be used\. Array-like and dict are transformed internally to a pandas DataFrame\. Optional: if missing, a DataFrame gets constructed under the hood using the other arguments\.', 'DataFrame containing the data to plot.', simplified_desc)
        
        # Simplify common patterns
        simplified_desc = re.sub(r'position marks along the ([xy]) axis in cartesian coordinates', r'position marks on \1-axis', simplified_desc)
        simplified_desc = re.sub(r'assign (\w+) to marks', r'set mark \1', simplified_desc)
        
        # Truncate very long descriptions
        if len(simplified_desc) > 200:
            sentences = simplified_desc.split('. ')
            simplified_desc = sentences[0] + '.'
        
        simplified.append(simplified_desc)
    
    return simplified

def process_file(input_file: str, output_file: str, batch_size: int = 10):
    """Process the entire file and simplify descriptions"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result_lines = []
    descriptions_to_process = []
    line_indices = []
    
    # First pass: collect all descriptions
    for i, line in enumerate(lines):
        field_name, field_type, description, indent, field_args = extract_field_info(line)
        
        if field_name and description:
            descriptions_to_process.append({
                'field_name': field_name,
                'field_type': field_type, 
                'description': description,
                'indent': indent,
                'field_args': field_args,
                'line_index': i
            })
            line_indices.append(i)
        
        result_lines.append(line)
    
    print(f"Found {len(descriptions_to_process)} field descriptions to simplify...")
    
    # Process descriptions in batches
    for i in range(0, len(descriptions_to_process), batch_size):
        batch = descriptions_to_process[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(descriptions_to_process)-1)//batch_size + 1}...")
        
        simplified_descriptions = simplify_descriptions_batch(batch)
        
        # Update the lines with simplified descriptions
        for j, simplified_desc in enumerate(simplified_descriptions):
            desc_info = batch[j]
            line_idx = desc_info['line_index']
            
            # Reconstruct the field line with simplified description
            new_field_args = re.sub(
                r'description="[^"]*(?:\\.[^"]*)*"',
                f'description="{simplified_desc}"',
                desc_info['field_args']
            )
            
            new_line = f"{desc_info['indent']}{desc_info['field_name']}: {desc_info['field_type']} = Field({new_field_args})\n"
            result_lines[line_idx] = new_line
    
    # Write the result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)
    
    print(f"Simplified descriptions written to: {output_file}")

def compare_descriptions(original_file: str, simplified_file: str, num_examples: int = 5):
    """Show before/after examples of simplified descriptions"""
    
    print(f"\n=== BEFORE/AFTER COMPARISON ===\n")
    
    with open(original_file, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
    
    with open(simplified_file, 'r', encoding='utf-8') as f:
        simplified_lines = f.readlines()
    
    examples_shown = 0
    for i, (orig_line, simp_line) in enumerate(zip(original_lines, simplified_lines)):
        if examples_shown >= num_examples:
            break
            
        orig_info = extract_field_info(orig_line)
        simp_info = extract_field_info(simp_line)
        
        if orig_info[0] and simp_info[0] and orig_info[2] != simp_info[2]:
            print(f"Field: {orig_info[0]}")
            print(f"BEFORE: {orig_info[2]}")
            print(f"AFTER:  {simp_info[2]}")
            print("-" * 80)
            examples_shown += 1

if __name__ == "__main__":
    input_file = r"P:\Coding\plotly_classes_reorganized.py"
    output_file = r"P:\Coding\plotly_classes_simplified.py"
    
    print("🤖 Starting description simplification...")
    print("🔑 Using GPT-4.1 for intelligent description simplification...")
    print()
    
    try:
        process_file(input_file, output_file)
        print("✅ Successfully simplified descriptions!")
        print(f"📁 Original file: {input_file}")
        print(f"📁 Simplified file: {output_file}")
        
        # Show examples
        compare_descriptions(input_file, output_file)
        
        print("\n🎯 Benefits for LLM usage:")
        print("- Removed verbose boilerplate text")
        print("- Kept essential functionality descriptions")
        print("- More concise and focused descriptions")
        print("- Easier for LLMs to parse and understand")
        
    except Exception as e:
        print(f"❌ Error: {e}") 