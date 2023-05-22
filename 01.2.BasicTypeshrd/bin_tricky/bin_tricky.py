import typing as tp


def find_median(nums1: tp.Sequence[int], nums2: tp.Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    m, n = len(nums1), len(nums2)
    if m > n:
        nums1, nums2, m, n = nums2, nums1, n, m
    if m != 0:
        mi, ma, half_len = 0, m, (m + n + 1) // 2
        while mi <= ma:
            i = (mi + ma) // 2
            j = half_len - i
            if i < m and nums2[j - 1] > nums1[i]:
                mi = i + 1
            elif i > 0 and nums1[i - 1] > nums2[j]:
                ma = i - 1
            else:
                if i == 0:
                    left = nums2[j - 1]
                elif j == 0:
                    left = nums1[i - 1]
                else:
                    left = max(nums1[i - 1], nums2[j - 1])
                if (m + n) % 2 == 1:
                    return left.__float__()
                if i == m:
                    right = nums2[j]
                elif j == n:
                    right = nums1[i]
                else:
                    right = min(nums1[i], nums2[j])

                return (left + right) / 2
        return 0.0
    else:
        if n % 2 == 0:
            return (nums2[n // 2 - 1] + nums2[n // 2]) / 2
        else:
            return nums2[n // 2].__float__()
