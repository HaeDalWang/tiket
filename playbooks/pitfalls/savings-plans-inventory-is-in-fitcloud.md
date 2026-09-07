# Savings Plans 조회는 FitCloud 포털에서 안내한다

## Risk

SP 구매 후 확인 방법을 물으면 **AWS 콘솔의 Savings Plans > Inventory 를 안내하기 쉽다.**
공식 문서가 그렇게 적혀 있어서 문서만 보고 답하면 그 경로가 나온다.

**우리 고객사는 대부분 그 화면을 볼 수 없다.** linked account 에서는 Billing 계열 조회가
Payer 정책으로 제한되는 경우가 많고, 실제로 고객이 문의에 "조회 권한이 없어 AWS 콘솔상으로
확인이 어렵다"고 먼저 밝히기도 한다.

## Known observation

- 2026-09-07, 티켓 164059(캠핑톡 SP 구매 문의)에서 실제로 발생했다.
  고객이 **문의 첫 문단에 조회 권한이 없다고 명시**했는데도 초안은 AWS 콘솔 Inventory 를
  안내했고, 이어서 "AWS 콘솔 조회 권한이 없는 경우에는 구매 완료 후 회신 부탁드립니다"로
  마무리했다. 고객이 스스로 확인할 수 있는 것을 우리에게 물어보게 만드는 답이 됐다.
- 실제 발송된 회신은 **FitCloud 빌링 포털 → Billings > Savings Plans > Inventory** 를
  안내했다. 고객이 직접 볼 수 있는 경로다.

## Required behavior

- **SP·RI 구매 후 확인 경로는 FitCloud 빌링 포털을 기본으로 안내한다.**
  `Billings > Savings Plans > Inventory`
- AWS 공식 문서의 콘솔 경로를 그대로 옮기기 전에, **그 고객이 그 화면을 볼 수 있는지**
  먼저 따진다. linked account 는 Cost Explorer·Budgets·Billing 조회가 막혀 있는 경우가 많다.
- 고객이 문의에서 **권한 제약을 이미 밝혔다면 그 제약을 답변이 반영해야 한다.**
  제약을 읽고도 못 쓰는 경로를 안내하면 왕복만 늘어난다.
- 구매 자체(AWS 콘솔 Billing and Cost Management > Savings Plans > Purchase)와
  **구매 후 조회(FitCloud)** 는 경로가 다르다. 둘을 섞지 않는다.
- 콘솔 화면 안내는 **한글 UI 명칭**으로 적고 필요하면 영문을 병기한다. 고객이 보는 화면과
  같은 단어를 써야 한다. 스크린샷이 텍스트 경로보다 빠른 경우가 많다.

## Verification before reuse

FitCloud 메뉴 구조는 바뀔 수 있다. 안내 전에 실제 포털에서 경로를 확인하고, 확인 날짜를
티켓에 남긴다. 경로가 바뀌었으면 이 문서에 날짜를 붙여 append 한다.
