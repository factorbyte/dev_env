class Solution:
    def twoSum(self, nums, target):
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i
        return []

sol = Solution()
result = sol.twoSum([2, 7, 11, 15], 9)
print(result)

# def twoSum(nums, target):
#     num_to_index = {}
#     for i, num in enumerate(nums):
#         complement = target - num
#         if complement in num_to_index:
#             return [num_to_index[complement], i]
#         num_to_index[num] = i
#     return []

# # 测试多组数据
# print(twoSum([2, 7, 11, 15], 9))   # 输出 [0, 1]
# print(twoSum([3, 2, 4], 6))        # 输出 [1, 2]
# print(twoSum([3, 3], 6))           # 输出 [0, 1]