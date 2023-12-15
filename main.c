#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <direct.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <time.h>
#include <tchar.h>

#define config_file_path "./config.cfg"
#define DATABASE_FILE_PATH "./database.CSV"
#define OLD_DATABASE_FILE_PATH "./old_database.CSV"
#define MAX_PATH_LEN 1000
#define MAX_LINE_LENGTH 1020
int refreashtime = 1800; // default 30 minutes
char VaultPath[MAX_PATH_LEN]; // vault full path
char masterpassword[MAX_PATH_LEN]; // master password
char backup_folder_Path[MAX_PATH_LEN] = ".\\backup"; // the path where the backup


// Structure to represent a file
typedef struct {
    char path[MAX_PATH_LEN];
    time_t lastModifiedTime;
} FileEntry;



void removeNewline(char *str) {
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }
}

/*########################
loading the cofig file
##########################*/
void create_config_file() {
    FILE *config;
    
    config = fopen(config_file_path,"w");
    if(config == NULL) {
        printf("an error accurand when creating the configuration 'config.cfg' file");
        exit(1);
    }

    // Get user input for the Vault path
    printf("Enter the Vault path: ");
    // we don't use scanf because it wont include any path if it includes a directory name that has a "space" in it. 
    // because scanf("%s",&path) will read till the space
    if (fgets(VaultPath, sizeof(VaultPath), stdin) == NULL) {
        printf("Error reading input.\n");
        exit(1);
    }

    // Remove the newline character if present
    removeNewline(VaultPath);


    printf("Enter backup folder path: ");
    if (fgets(backup_folder_Path, sizeof(backup_folder_Path), stdin) == NULL) {
        printf("Error reading input.\n");
        exit(1);
    }
    // Remove the newline character if present
    removeNewline(backup_folder_Path);

    printf("Enter password: ");
    if (fgets(masterpassword, sizeof(masterpassword), stdin) == NULL) {
        printf("Error reading input.\n");
        exit(1);
    }
    // Remove the newline character if present
    removeNewline(masterpassword);

    // setting the refreashe rate in seconds. this will be the time in which the program will update the vault database
    printf("\nEnter a refreash time in seconds (eg. if youy enter 1800 the program will refreash every 30min): ");
    scanf("%i", &refreashtime);

    // creating and closing the config file
    fprintf(config, "%s\n%i\n%s", VaultPath, refreashtime, masterpassword);
    fclose(config);
}

void load_config_file() {
    FILE *config;
    
    config =fopen(config_file_path,"r");
    //check if the config file does exist or not
    if(config == NULL) {
        // creating the config.cfg file
        create_config_file();

        // reloading the config file
        return load_config_file();
    };


    fgets(VaultPath, sizeof(VaultPath), config); // get path
    // Remove the newline character if present
    removeNewline(VaultPath);

    fgets(backup_folder_Path, sizeof(backup_folder_Path), config);
    removeNewline(backup_folder_Path);

    fgets(masterpassword, sizeof(masterpassword), config);
    removeNewline(masterpassword);


    fscanf(config, "%i", &refreashtime); // get refreash time
    fclose(config);


    printf("vault path:%s\nrefreash time:%i\n", VaultPath,refreashtime);
}




/*########################
loading the database
##########################*/
void addToDatabase(const char *path, time_t lmt) {
    FILE *databaseFile = fopen(DATABASE_FILE_PATH, "a");
    if (databaseFile == NULL) {
        perror("Error opening database file");
        exit(EXIT_FAILURE);
    }

    fprintf(databaseFile, "%s,%ld\n", path, (long)lmt);

    fclose(databaseFile);
}

void createDatabaseFile(const char *path) {
    DIR *dir;
    struct dirent *entry;

    if ((dir = opendir(path)) != NULL) {
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
                char filePath[MAX_PATH_LEN];
                snprintf(filePath, sizeof(filePath), "%s\\%s", path, entry->d_name);

                struct stat fileStat;
                if (stat(filePath, &fileStat) == 0) {
                    if (S_ISDIR(fileStat.st_mode)) {
                        createDatabaseFile(filePath);
                    } else if (S_ISREG(fileStat.st_mode)) {
                        addToDatabase(filePath, fileStat.st_mtime);
                    }
                } else {
                    printf("%s",filePath);
                    perror("Error getting file information");
                }
            }
        }
        closedir(dir);
    } else {
        perror("Error opening directory");
        exit(EXIT_FAILURE);
    }
}








/*#######################
Archive files
#########################*/
void archivefiles(char *backupfolderPath) {
    char command[1000];

    sprintf(command, ".\\7z_x64\\7za.exe a \"%s\\vault.7z\" -p\"%s\" -mhe=on \"%s\\*\"", backupfolderPath, masterpassword, backupfolderPath);
    // Execute the command
    int result = system(command);

    // Check the result of the command execution
    if (result == 0) {
        printf("archiving successfully.\n");
    } else {
        printf("archiving failed to execute.\n");
    }
}




void createFolderIfNotExists(const char *folderPath) {
    struct stat st = {0};

    // Check if the folder exists
    if (stat(folderPath, &st) == -1) {
        // If the folder doesn't exist, create it
        if (mkdir(folderPath) == -1) {
            perror("Error creating folder");
            exit(EXIT_FAILURE);
        }
    }
}

/*########################
Comparing
##########################*/
char* createFolderWithTime(const char *basePath) {
    // Get the current time in Unix format
    time_t currentTime = time(NULL);

    // Convert the time to a string for the folder name
    char folderName[20]; // Assuming a maximum of 20 characters for the folder name
    strftime(folderName, sizeof(folderName), "%Y%m%d%H%M%S", localtime(&currentTime));

    // Construct the full path for the new folder
    char folderPath[256]; // Assuming a maximum path length
    snprintf(folderPath, sizeof(folderPath), "%s\\%s", basePath, folderName);

    // Check if the folder exists
    struct stat st = {0};
    if (stat(folderPath, &st) == -1) {
        // If the folder doesn't exist, create it
        if (mkdir(folderPath) == -1) {
            perror("Error creating folder");
            exit(EXIT_FAILURE);
        }
        printf("Folder created: %s\n", folderPath);
    } else {
        printf("Folder already exists: %s\n", folderPath);
    }
    
    // Return a dynamically allocated copy of the folder path
    return strdup(folderPath);
}



// Function to create folders and subfolders if they don't exist
void createDirectories(const char *path) {
    char *token;
    char *splicedPath = strdup(path); // Duplicate the original path for modification
    char *splicedPath2 = strdup(path); // Duplicate the original path for modification
    char reconstructedPath[MAX_PATH_LEN];

    if (splicedPath == NULL) {
        perror("Memory allocation error");
        exit(EXIT_FAILURE);
    }

    reconstructedPath[0] = '\0';  // Initialize the reconstructed path to an empty string

    // Tokenize the path using '\\' as the delimiter
    token = strtok(splicedPath, "\\");

    int count = 0;
    // Reconstruct the path part by part
    while (token != NULL) {
        strcat(reconstructedPath, token);
        count++;
        token = strtok(NULL, "\\");

        // If the next token is not NULL, append a backslash
        if (token != NULL) {
            strcat(reconstructedPath, "\\");
        }
    }

    token = strtok(splicedPath2, "\\");
    reconstructedPath[0] = '\0';
    for (int i= 1; i<count;i++) {
        strcat(reconstructedPath, token);
        if (strcmp(reconstructedPath, "C:") != 0) {
            printf("%s\n",reconstructedPath);
            createFolderIfNotExists(reconstructedPath);
        }
        token = strtok(NULL, "\\");

        // If the next token is not NULL, append a backslash
        if (token != NULL) {
            strcat(reconstructedPath, "\\");
        }

    }
    // Free the duplicated path
    free(splicedPath);
}

void copyFile(const char *sourcePath, const char *destinationPath) {
    createDirectories(destinationPath);

    FILE *sourceFile = fopen(sourcePath, "rb");
    FILE *destinationFile = fopen(destinationPath, "wb");

    if (sourceFile == NULL || destinationFile == NULL) {
        perror("Error opening files");
        exit(EXIT_FAILURE);
    }

    char buffer[1024];
    size_t bytesRead;

    while ((bytesRead = fread(buffer, 1, sizeof(buffer), sourceFile)) > 0) {
        fwrite(buffer, 1, bytesRead, destinationFile);
    }

    fclose(sourceFile);
    fclose(destinationFile);
}






char *replaceSubstring(const char *original, const char *substring, const char *replacement) {
    char *result = strdup(original);
    if (result == NULL) {
        perror("Memory allocation error");
        exit(EXIT_FAILURE);
    }

    char *found = strstr(result, substring);

    while (found != NULL) {
        // Calculate the lengths of the parts before and after the substring
        size_t prefixLength = found - result;
        size_t suffixLength = strlen(found + strlen(substring));

        // Create a new string with the replaced substring
        char *newString = (char *)malloc(prefixLength + strlen(replacement) + suffixLength + 1);
        if (newString == NULL) {
            perror("Memory allocation error");
            free(result);
            exit(EXIT_FAILURE);
        }

        // Copy the prefix
        strncpy(newString, result, prefixLength);
        newString[prefixLength] = '\0';

        // Concatenate the replacement
        strcat(newString, replacement);

        // Concatenate the suffix
        strcat(newString, found + strlen(substring));

        // Update the result string
        free(result);
        result = newString;

        // Find the next occurrence
        found = strstr(result, substring);
    }

    return result;
}

void compareDatabases(const char *oldDatabasePath, const char *newDatabasePath) {
    char *backupfolderPath = createFolderWithTime(backup_folder_Path);
    FILE *detetedfile;
    char deletefilename[MAX_PATH_LEN];
    strcpy(deletefilename, backupfolderPath);
    strcat(deletefilename, "\\.detetedfiles");
    detetedfile = fopen(deletefilename, "w");

    // Read entries from the old database
    FILE *oldDatabaseFile = fopen(oldDatabasePath, "r");
    if (oldDatabaseFile == NULL) {
        fclose(oldDatabaseFile);
        // create an empty database
        oldDatabaseFile = fopen(oldDatabasePath, "w");
        fclose(oldDatabaseFile);

        oldDatabaseFile = fopen(oldDatabasePath, "r");

    }

    // Create a dynamic array to store old database entries
    FileEntry *oldEntries = NULL;
    size_t oldEntriesCount = 0;

    char line[MAX_PATH_LEN + 20]; // Assuming a maximum path length and time_t length
    while (fgets(line, sizeof(line), oldDatabaseFile) != NULL) {
        char path[MAX_PATH_LEN];
        time_t lastModifiedTime;
        if (sscanf(line, "%[^,],%ld", path, &lastModifiedTime) == 2) {
            // Allocate memory for a new entry
            oldEntries = realloc(oldEntries, (oldEntriesCount + 1) * sizeof(FileEntry));
            if (oldEntries == NULL) {
                perror("Memory allocation error");
                exit(EXIT_FAILURE);
            }

            // Copy data to the new entry
            strncpy(oldEntries[oldEntriesCount].path, path, sizeof(oldEntries[oldEntriesCount].path));
            oldEntries[oldEntriesCount].lastModifiedTime = lastModifiedTime;

            oldEntriesCount++;
        } else {
            fprintf(stderr, "Error parsing line in old database: %s", line);
        }
    }

    fclose(oldDatabaseFile);

    // Read entries from the new database
    FILE *newDatabaseFile = fopen(newDatabasePath, "r");
    if (newDatabaseFile == NULL) {
        perror("Error opening new database file");
        exit(EXIT_FAILURE);
    }

    char newLine[MAX_PATH_LEN + 20]; // Assuming a maximum path length and time_t length

    while (fgets(newLine, sizeof(newLine), newDatabaseFile) != NULL) {
        char path[MAX_PATH_LEN];
        time_t lastModifiedTime;
        if (sscanf(newLine, "%[^,],%ld", path, &lastModifiedTime) == 2) {
            // Check if the entry exists in the old database
            int found = 0;
            for (size_t i = 0; i < oldEntriesCount; i++) {
                if (strcmp(path, oldEntries[i].path) == 0) {
                    found = 1;

                    // Check if the last modification time is different
                    if (lastModifiedTime != oldEntries[i].lastModifiedTime) {
                        printf("Modified: %s\n", path);
                        copyFile(path, replaceSubstring(path, VaultPath, backupfolderPath));
                    }

                    // Remove the entry from the old entries list
                    oldEntries[i] = oldEntries[oldEntriesCount - 1];
                    oldEntriesCount--;

                    break;
                }
            }

            // If the entry is not found in the old database, it's a new file
            if (!found) {
                printf("New: %s\n", path);
                copyFile(path, replaceSubstring(path, VaultPath, backupfolderPath));
            }
        } else {
            fprintf(stderr, "Error parsing line in new database: %s", newLine);
        }
    }

    fclose(newDatabaseFile);

    // Any remaining entries in oldEntries are files that were in the old database but not in the new one
    for (size_t i = 0; i < oldEntriesCount; i++) {
        printf("Deleted: %s\n", oldEntries[i].path);
        fprintf(detetedfile,"%s\n", replaceSubstring(oldEntries[i].path, VaultPath, ""));
    }
    fclose(detetedfile);

    // Free allocated memory
    free(oldEntries);

    archivefiles(backupfolderPath);
}


void relocate_database_to_old() {
    FILE *DatabaseFile = fopen(DATABASE_FILE_PATH, "r");
    FILE *oldDatabaseFile = fopen(OLD_DATABASE_FILE_PATH, "w");

    for (char x = fgetc(DatabaseFile); x!=EOF; x = fgetc(DatabaseFile)) {
        fputc(x,oldDatabaseFile);
    }

    fclose(DatabaseFile);
    fclose(oldDatabaseFile);
}


int main() {

    /* starting the program */
    load_config_file(); // this fuction sets the 'refreashtime' and 'VaultPath' variables
    
    FILE *databaseFile = fopen(DATABASE_FILE_PATH, "w"); // reset the database
    fclose(databaseFile);
    createDatabaseFile(VaultPath);

    createFolderIfNotExists(backup_folder_Path);
    while (1) {
        compareDatabases(OLD_DATABASE_FILE_PATH, DATABASE_FILE_PATH);
        relocate_database_to_old();
        sleep(refreashtime);
    }

    // printf("Files and folders in directory '%s':\n", VaultPath);
    // listFilesAndFolders(VaultPath);

    return 0;
}
