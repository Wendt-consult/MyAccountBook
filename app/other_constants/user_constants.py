#****************************************************************************
#   GST REGISTRATION TYPE
#****************************************************************************
GST_REG_TYPE = (
    (0, 'Not Applicable'),
    (1, 'GST Registered-Regular'),
    (2, 'GST Registered-Composition'),
    (3, 'GST Unregistered'),
    (4, 'Consumer'),
    (5, 'Overseas'),
    (6, 'SEZ'),
    (7, 'Deemed Exports -EOU’s, STP’s , EHTP’s etc'),
    (8, 'Composite GST')
)

org_GST_REG_TYPE = (
    (1, 'GST Registered-Regular'),
    (2, 'GST Registered-Composition'),
    (4, 'Consumer'),
    (6, 'SEZ'),
    (7, 'Deemed Exports -EOU’s, STP’s , EHTP’s etc'),
    (8, 'Composite GST')
)

#****************************************************************************
#   RECORD STATUS CODES
#****************************************************************************
IS_TRUE = ((True, 'YES'), (False, 'NO'))

IS_NUM_CHOICE = ((1, 'YES'), (0, 'NO'))

#****************************************************************************
#   ORGANIZATION TYPE
#****************************************************************************
# ORGANIZATION_TYPE = (
#     (1, 'Individual'),
#     (2, 'Proprietorship'),
#     (4, 'Partnership'),
#     (5, 'Trust'),
#     (6, 'Private Limited'),
#     (7, 'Public Limited'),
#     (8, 'Overseas Organisation'),
#     (9, 'Government Organisation'),
# )
ORGANIZATION_TYPE = (
    (1, 'Individual'),
    (2, 'Proprietorship'),
    (4, 'Partnership'),
    (5, 'Trust'),
    (6, 'Private Limited'),
    (7, 'Public Limited'),
    (8, 'Overseas Organisation'),
    (9, 'Government Organisation'),
    (10, 'Others'),
)
#****************************************************************************
#   
#****************************************************************************

SALUTATIONS = (
    (0, 'Mr.'),
    (1, 'Mrs.'),
    (2, 'Miss'),
    (3, 'Dr.'),
    (4, 'Ms.'),
    # (5, 'Prof.'),
    # (6, 'Rev.'),
    # (7, 'Lady'),
    # (8, 'Sir'),
    # (9, 'Capt.'),
    # (10, 'Major'),
    # (11, 'Lt.-Col.'),
    # (12, 'Col.'),
    # (13, 'Lady'),
    # (14, 'Lt.-Cmdr.'),
    # (15, 'The Hon.'),
    # (16, 'Cmdr.'),
    # (17, 'Flt. Lt.'),
    # (18, 'Brgdr.'),
    # (19, 'Judge'),
    # (20, 'Lord'),
    # (21, 'The Hon. Mrs'),
    # (22, 'Wng. Cmdr.'),
    # (23, 'Group Capt.'),
    # (24, 'Rt. Hon. Lord'),
    # (25, 'Revd. Father'),
    # (26, 'Revd Canon'),
    # (27, 'Maj.-Gen.'),
    # (28, 'Air Cdre.'),
    # (29, 'Viscount'),
    # (30, 'Dame'),
    # (31, 'Rear Admrl.')
)

#============================================================================
#
#============================================================================

CUSTOMER_TYPE = (
    (1, 'Customer'),
    (2, 'Vendor'),
    (3, 'Employee'),  
    (4, 'Customer and Vendor')
)

#============================================================================
#
#============================================================================

IS_SUB_CUSTOMER = (
    (1, 'Parent Customer'),
    (2, 'Bill With Parent'),
    (3, 'Bill with Customer'),
)

LINE_OF_ORGANISATION = (
    (1, 'Accounting and Bookkeeping'),
    (2, 'Advertising'),
    (3, 'Manufacturing'),
    (4, 'Agriculture'),
    (5, 'Photography'),
    (6, 'Automotive Sales and Repair'),
    (7, 'Church and Religious Organizationg'),
    (8, 'Construction'),
    (9, 'Agriculture'),
    (10, 'Design, Architecture and Engineering'),
    (11, 'Financial Services'),
    (12, 'Information Technology'),
    (13, 'Insurance Agency and Broker'),
    (14, 'Legal Services'),
    (15, 'Lodging such as Hotels and Motels'),
    (16, 'Medical'),
    (17, 'Non-Profit'),
    (18, 'Property Management'),
    (19, 'Repair and Maintenance'),
    (20, 'Restaurant'),
    (21, 'Retail Shop and Online Commerce'),
    (22, 'Sales: Independent Agent'),
    (23, 'Transportation'),
    (24, 'Wholesale Distribution and Sales'),
)

#============================================================================
# Phone number country code
#============================================================================

PHONE_COUNTRY_CODE = (
    (1, '+1'),
    (2, '+7'),
    (4, '+7'),
    (5, '+20'),
    (6, '+27'),
    (7, '+30'),
    (8, '+31'),
    (9, '+32'),
    (10, '+33'),
    (11, '+34'),
    (12, '+36'),
    (13, '+39'),
    (14, '+40'),
    (15, '+41'),
    (16, '+43'),
    (17, '+44'),
    (18, '+45'),
    (19, '+46'),
    (20, '+47'),
    (21, '+48'),
    (22, '+49'),
    (23, '+51'),
    (24, '+52'),
    (25, '+53'),
    (26, '+54'),
    (27, '+55'),
    (28, '+56'),
    (29, '+57'),
    (30, '+58'),
    (31, '+60'),
    (32, '+61'),
    (33, '+61'),
    (34, '+62'),
    (35, '+63'),
    (36, '+64'),
    (37, '+64'),
    (38, '+65'),
    (39, '+66'),
    (40, '+81'),
    (41, '+82'),
    (42, '+84'),
    (43, '+86'),
    (44, '+90'),
    (45, '+91'),
    (46, '+92'),
    (47, '+93'),
    (48, '+94'),
    (49, '+98'),


)