// leetcode 105: construct binary tree from preorder and inorder traversal (medium)

#include <iostream>
/*
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */

class Solution {

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        /*
        At every recursive step:
            The root is the first element of the current preorder range
            The root splits the inorder array into left and right subtrees

        Recursive construction:
            Find the root value in the inorder array to determine subtree boundaries
            Recursively build the left subtree using:
                preorder indices: next element after root up to left subtree size
                inorder indices: start to root's index - 1
            Recursively build the right subtree using:
                preorder indices: after left subtree section to end
                inorder indices: root's index + 1 to end
            Return the root with attached left and right subtrees
        */

        return helper(preorder, 0, preorder.size() - 1, inorder, 0, inorder.size() - 1);
    }

private:
    TreeNode* helper(vector<int>& preorder, int preStart, int preEnd, vector<int>& inorder, int inStart, int inEnd) {
        if (preStart > preEnd || inStart > inEnd) return nullptr;

        TreeNode* root = new TreeNode(preorder[preStart]);

        int inRoot = inStart;
        while (inorder[inRoot] != preorder[preStart]) {
            inRoot++;
        }

        int leftSize = inRoot - inStart;

        root->left = helper(preorder, preStart + 1, preStart + leftSize, inorder, inStart, inRoot - 1);
        root->right = helper(preorder, preStart + leftSize + 1, preEnd, inorder, inRoot + 1, inEnd);

        return root;
    }
};
