# leetcode 614: second degree follower (medium)
# SQL problem

SELECT 
    f1.followee AS follower,
    COUNT(*) AS num
FROM Follow f1
WHERE f1.followee IN (
    SELECT DISTINCT follower 
    FROM Follow f2
)
GROUP BY f1.followee
ORDER BY follower;
