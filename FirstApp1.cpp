#include "pch.h"
#include <stdio.h>  // printf, fopen_s, fgets, fclose 함수를 사용하기 위해!
#include <stdlib.h> // srand
#include <time.h> 
#include "tipsware.h"

#define MAX_NAME_LEN 50
#define MAX_MENU_LEN 400
#define FONT_OVERWATCH "koverwatch"

#define GOTO_MAIN_BTN 9999

typedef struct MenuData {
    char name[MAX_NAME_LEN];// 가게이름
} M_DATA;


void print_main_buttons() {
    const char* p_btn_name[13] = {"한식", "양식", "중식", "일식", "카페", "디저트", "패스트푸드", "치킨", "분식", "퓨전", "술집", "기타", "지정 뽑기"};
    unsigned int x = 200, y = 90;
    unsigned int btn_ids = 1000; // 메뉴 버튼의 id는 1000 ~ 1012 로 사용
    for (int i = 0; i < 13; i++, btn_ids++, y += 50) {
        if (i == 6) { x = 500; y = 90; }
        CreateButton(p_btn_name[i], x, y, 200, 30, btn_ids);

        // 버튼의 외관
        void* btn_id = FindControl(btn_ids);
        SetCtrlFont(btn_id, FONT_OVERWATCH, 20, 0); 
        ChangeCtrlColor(btn_id, RGB(252, 248, 240), RGB(255, 220, 150), RGB(255, 220, 150), RGB(0, 0, 0));
    }
    ShowDisplay();
}   

void side_menu() {
    ChangeWorkSize(800, 500); // 작업 영역을 설정한다.
    Clear(0, RGB(252, 248, 240));  // 작업 영역을 RGB(252, 248, 240) 색으로 채운다!
    Rectangle(0, 0, 100, 500, RGB(255, 220, 150), RGB(255, 220, 150));
    SelectFontObject(FONT_OVERWATCH, 26, 0);
    TextOut(7, 10, RGB(0, 0, 0), "SSU");
    TextOut(7, 35, RGB(0, 0, 0), "Meal");
    TextOut(7, 60, RGB(0, 0, 0), "Proposal");

    ShowDisplay(); // 정보를 윈도우에 출력한다.
}


void ReadFileDataToListBox(void* ap_list_box, const char* ap_file_name)
{
    FILE* p_file = NULL;  // 파일을 열어서 사용할 파일 포인터!
    // fopen_s 함수를 사용하여 파일을 텍스트 형식의 읽기 모드로 연다!
    // 이 함수는 파일 열기에 성공했다면 0을 반환한다.
    srand(time(NULL));

    if (0 == fopen_s(&p_file, ap_file_name, "rt")) {
        // 파일에서 한 줄의 정보를 읽어서 저장할 변수와
        // 쉼표를 기준으로 분리한 문자열을 저장할 변수
        char one_line_string[256], str[64], * p_pos;
        // 이름을 저장할 변수와 ListBox에 추가할 문자열을 구성할 배열
        char name[64], insert_str[256];
        
        int i, rdm = 0;
        // 파일에서 한 줄의 데이터를 읽는다.
        // 하지만 첫 줄은 타이틀 정보라서 처리하지 않고 넘어간다.
        if (NULL != fgets(one_line_string, 256, p_file)) {
            // 파일의 끝까지 학생별 성적 정보를 읽어들인다.
            for (i = 0; NULL != fgets(one_line_string, 256, p_file); i++) {
                p_pos = GetNextString(one_line_string, ',', str); // 학번을 읽는다.
                strcpy_s(name, 64, str);
                // ListBox에 추가할 문자열을 구성한다. 화면에 출력되지 않고 insert_str 배열에
                // 문자열이 저장됩니다.
                sprintf_s(insert_str, 256, "%s", name);
                // insert_str에 저장된 문자열을 ListBox에 추가한다.
                ListBox_InsertString(ap_list_box, i, insert_str, 0);
            }

        }
        fclose(p_file);  // 파일을 닫는다.
    }
}

void OnCommand(INT32 a_ctrl_id, INT32 a_notify_code, void* ap_ctrl) {
    
    if (a_ctrl_id >= 1000 && a_ctrl_id <= 1012) { // 메뉴 버튼일 경우
        const char* csv_name[12] = { "cate/kor.csv", "cate/wst.csv", "cate/chn.csv", "cate/jpn.csv", "cate/cafe.csv", "cate/cake.csv", "cate/fast.csv",
                          "cate/chick.csv", "cate/mil.csv", "cate/fusion.csv", "cate/alc.csv", "cate/etc.csv" };
        void* p = CreateListBox(130, 80, 640, 400, 2000, NULL);  // 리스트 박스를 생성한다.
        ChangeCtrlColor(p, RGB(222, 210, 177), RGB(252, 248, 240), RGB(252, 248, 240), RGB(0, 0, 0));
        SetCtrlFont(p, FONT_OVERWATCH, 13, 0);
        if (a_ctrl_id != 1012) // 지정 뽑기가 아닌 경우
        {
            ReadFileDataToListBox(p, csv_name[a_ctrl_id - 1000]); // 파일에서 성적 정보를 읽어서 ListBox에 추가한다.
            int num_of_box = ListBox_GetCount(p), idx = 0;
            char rdm_select[256];
            srand(time(NULL));
            idx = rand() % num_of_box;
            ListBox_GetText(p, idx, rdm_select, 128);

            char cate[64];
            GetCtrlName(FindControl(a_ctrl_id), cate, 64);
            TextOut(130, 20, "%s", cate);
            SelectFontObject(FONT_OVERWATCH, 20, 0);
            TextOut(130, 55, "- 이 식당은 어떤가요? : %s ", rdm_select);
        }
        else { // 지정 뽑기 메뉴일 경우
            DestroyControl(FindControl(2000));
            void* p = CreateListBox(130, 80, 640, 320, 2000, NULL);  // 리스트 박스를 생성한다.
            CreateEdit(130, 430, 640, 50, 2003, 0);
            ChangeCtrlColor(FindControl(2003), RGB(252, 248, 240), RGB(255, 220, 150), RGB(255, 220, 150), RGB(0, 0, 0));
            ChangeCtrlColor(p, RGB(222, 210, 177), RGB(252, 248, 240), RGB(252, 248, 240), RGB(0, 0, 0));
            void *edit_p = CreateEdit(130, 20, 545, 40, 2001, 0);
            void *btn_p_add = CreateButton("추가", 680, 20, 35, 40, 1030); // 1030: 추가 버튼 id
            void *btn_p_result = CreateButton("뽑기", 720, 20, 50, 40, 1031); // 1031: 추출 버튼 id
            SetCtrlFont(edit_p, FONT_OVERWATCH, 24, 0);
            SetCtrlFont(btn_p_add, FONT_OVERWATCH , 20, 0);
            SetCtrlFont(btn_p_result, FONT_OVERWATCH, 20, 0);
        }
        unsigned int btn_ids = 1000;
        for (int i = 0; i < 13; i++, btn_ids++) {
            DestroyControl(FindControl(btn_ids));
        }
        void* btn_p = CreateButton("메뉴", 5, 450, 90, 40, GOTO_MAIN_BTN); // 메인화면으로 돌아가는 버튼
        SetCtrlFont(btn_p, FONT_OVERWATCH, 20, 0);
        ChangeCtrlColor(btn_p, RGB(252, 248, 240), RGB(255, 220, 150), RGB(255, 220, 150), RGB(0, 0, 0));

        ShowDisplay();
    }
    if (a_ctrl_id == 1030) { // 지정뽑기 - 추가 버튼
        char str[256];
        GetCtrlName(FindControl(2001), str, 64);
        SetCtrlName(FindControl(2001), "");
        ListBox_InsertString(FindControl(2000), -1, str, 0);
    }
    if (a_ctrl_id == 1031) { // 지정뽑기 - 결과 버튼
        int num_of_box = ListBox_GetCount(FindControl(2000)), idx = 0;
        char rdm_select[256];
        srand(time(NULL));
        idx = rand() % num_of_box;
        ListBox_GetText(FindControl(2000), idx, rdm_select, 128);
        //void* result_p = CreateEdit(130, 430, 640, 50, 2003, 0);
        SetCtrlName(FindControl(2003), rdm_select);
        SetCtrlFont(FindControl(2003), FONT_OVERWATCH, 25, 0);
        ChangeCtrlColor(FindControl(2003), RGB(252, 248, 240), RGB(255, 220, 150), RGB(255, 220, 150), RGB(0, 0, 0));
    }
    if (a_ctrl_id == 9999) {
        Clear();
        side_menu();
        DestroyControl(FindControl(9999)); // 왼쪽 하단 메뉴 버튼 삭제
        DestroyControl(FindControl(2000)); // ListBox 삭제
        DestroyControl(FindControl(2001)); // 지정뽑기 - 에딧컨트롤 삭제
        DestroyControl(FindControl(1030)); // 지정뽑기 - 추가 버튼
        DestroyControl(FindControl(1031)); // 지정뽑기 - 결과 버튼
        DestroyControl(FindControl(2003)); // 지정뽑기 - 결과 에딧컨트롤 삭제
        print_main_buttons();
    }
    /*else {
        ::MessageBox(gh_main_wnd, "잘못된 버튼 입니다",
            "생성된 버튼 없음!", MB_ICONSTOP);
    }*/
}

CMD_MESSAGE(OnCommand)

int main()
{
    side_menu();
    print_main_buttons();
    ShowDisplay(); // 정보를 윈도우에 출력한다.
    return 0;
}