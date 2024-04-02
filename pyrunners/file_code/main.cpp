class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());

        vector<vector<int>> v;

        for(int help = 0; help < nums.size(); ++help) {
            if(help > 0 && nums[help] == nums[help-1]) continue;
            
            int left = help + 1;
            int right = nums.size() - 1;
            while(left < right) {
                int sum = nums[help] + nums[left] + nums[right];
                if(sum < 0) {
                    ++left;
                } else if(sum > 0) {
                    --right;
                } else {
                    v.push_back({nums[help], nums[left], nums[right]});
                    while(left < right && nums[left] == nums[left+1]) ++left;
                    while(left < right && nums[right] == nums[right-1]) --right;
                    ++left; --right;
                }
            }
        }
        return v;
    }
};