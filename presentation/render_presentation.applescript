on run argv
    set inputPath to item 1 of argv
    set outputPath to item 2 of argv
    tell application "Keynote"
        set deck to open (POSIX file inputPath)
        with timeout of 120 seconds
            export deck to (POSIX file outputPath) as PDF
        end timeout
        close deck saving no
    end tell
end run
