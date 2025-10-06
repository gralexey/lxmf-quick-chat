# LXMF Quick Chat

A lightweight chat script for NomadNet nodes.

## How to Use

1. **Copy files**  
   Place all provided files into your NomadNet storage directory (or your preferred storage location):
   ```
   ~/.nomadnetwork/storage/pages/
   ```

2. **Make the script executable**  
   Run:
   ```
   chmod +x index.mu
   ```

3. **Verify the Python interpreter**

    Ensure that the first line of the script points to the correct Python interpreter on your system:
    ```
    #!/usr/bin/python
    ```
    Adjust the path if necessary (e.g., to `/usr/bin/python3`) to match your environment.

You're ready to go!

<img width="1080" alt="Screenshot 2025-10-06 at 19 17 34" src="https://github.com/user-attachments/assets/b66c74b5-4512-4425-8832-0f3e96be0b23" />


## Identification

This script can automatically pull your announced name if you identify yourself:

- **MeshChat**: click the fingerprint button to identify yourself
- **NomadNet**: save a node and set 'identify when connecting' in the node settings

When identified, your name will appear in send message box instead of guest placeholder.

## Troubleshooting

If something doesn't work, check errors from inside NomadNet app.

