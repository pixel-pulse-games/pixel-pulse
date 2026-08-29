import os
import re
import glob

def merge_part_files():
    print("Searching for split .part files...")
    
    # Match files ending in .part00, .part01, etc.
    part_pattern = re.compile(r'^(.*\.part)\d+$')
    all_files = glob.glob('./**/*.part*', recursive=True)
    
    # Identify unique base file groups
    file_groups = set()
    for f in all_files:
        match = part_pattern.match(f)
        if match:
            file_groups.add(match.group(1))
            
    if not file_groups:
        print("No .part files found to reconstruct!")
        return

    for base_part in file_groups:
        # Determine the original filename by stripping '.part' from the match group
        original_filename = base_part[:-5] 
        print(f"\nReconstructing: {original_filename}")
        
        # Find all matching pieces for this specific file group
        pieces = sorted(glob.glob(f"{base_part}[0-9]*"))
        
        try:
            with open(original_filename, 'wb') as output_file:
                for piece in pieces:
                    print(f" -> Appending: {os.path.basename(piece)}")
                    with open(piece, 'rb') as f_piece:
                        output_file.write(f_piece.read())
            
            # Verification check
            if os.path.exists(original_filename) and os.path.getsize(original_filename) > 0:
                print(f"✅ Successfully restored: {original_filename}")
                # Optional: Delete the parts to clean up space
                for piece in pieces:
                    os.remove(piece)
                print("🧹 Cleaned up temporary .part files.")
            else:
                print(f"❌ Failed to reconstruct {original_filename}")
                
        except Exception as e:
            print(f"❌ Error stitching {original_filename}: {e}")

if __name__ == "__main__":
    merge_part_files()
    input("\nPress Enter to exit...")
