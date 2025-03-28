-���� 2�7
Ytype.googleapis.com/google.internal.chrome.optimizationguide.v1.SegmentationModelMetadata�6 (0R*field_form_control_typeR*total_field_countR*multiline_field_countR*time_spent_on_pageR��
�WITH event_ids AS (SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'CCC33F79ECE7363D' AND metrics.metric_value IN (0, 14)) SELECT IFNULL(SUM(metric_value), 0) FROM metrics INNER JOIN event_ids ON metrics.event_id = event_ids.event_id WHERE metrics.metric_hash = '4E7D579594EB8315';!
��������'������վN�������"words_writtenR��
�WITH event_ids AS (SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'CCC33F79ECE7363D' AND metrics.metric_value IN (0, 14)) SELECT IFNULL(SUM(metric_value), 0) FROM metrics INNER JOIN event_ids ON metrics.event_id = event_ids.event_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5';"
 ��������'���������ڀ���"editing_timeR��
uSELECT COUNT(metric_value) FROM metrics WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 45;
��������'
��ڀ���"editing_sessionsR��
vSELECT COUNT(metric_value) FROM metrics WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 120;
��������'
��ڀ���"long_editing_sessionsR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0) SELECT COUNT(metric_value) FROM metrics INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 45;
��������'
��ڀ���
 "
nameorigin"editing_sessions_on_siteR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0) SELECT COUNT(metric_value) FROM metrics INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 120;
��������'
��ڀ���
 "
nameorigin"long_editing_sessions_on_siteR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0), event_ids_for_field AS ( SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'AE239414CC02813B' AND metrics.metric_value = ? ), event_ids_for_form AS ( SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = '42D464F8DC98BC83' AND metrics.metric_value = ? ) SELECT COUNT(metric_value) FROM metrics INNER JOIN event_ids_for_field ON metrics.event_id = event_ids_for_field.event_id INNER JOIN event_ids_for_form ON metrics.event_id = event_ids_for_form.event_id INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 45;+
)��������'���䍟��B����̂呮��ڀ���
 "
nameorigin$
"
namefield_signature#
"
nameform_signature"editing_sessions_on_fieldR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0), event_ids_for_field AS ( SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'AE239414CC02813B' AND metrics.metric_value = ? ), event_ids_for_form AS ( SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = '42D464F8DC98BC83' AND metrics.metric_value = ? ) SELECT COUNT(metric_value) FROM metrics INNER JOIN event_ids_for_field ON metrics.event_id = event_ids_for_field.event_id INNER JOIN event_ids_for_form ON metrics.event_id = event_ids_for_form.event_id INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5' AND metrics.metric_value > 120;+
)��������'���䍟��B����̂呮��ڀ���
 "
nameorigin$
"
namefield_signature#
"
nameform_signature"long_editing_sessions_on_fieldR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0), event_ids AS (SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'CCC33F79ECE7363D' AND metrics.metric_value IN (0, 14)) SELECT IFNULL(SUM(metric_value), 0) FROM metrics INNER JOIN event_ids ON metrics.event_id = event_ids.event_id INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = 'CE71BF280B4EB4B5';"
 ��������'���������ڀ���
 "
nameorigin"editing_time_on_siteR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0), event_ids AS (SELECT DISTINCT event_id FROM metrics WHERE metrics.metric_hash = 'CCC33F79ECE7363D' AND metrics.metric_value IN (0, 14)) SELECT IFNULL(SUM(metric_value), 0) FROM metrics INNER JOIN event_ids ON metrics.event_id = event_ids.event_id INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = '4E7D579594EB8315';!
��������'������վN�������
 "
nameorigin"words_typed_on_siteR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0) SELECT COUNT(id) FROM metrics INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = '64BD7CCE5A95BF00';
���ʖ����	�������d
 "
nameorigin"page_loads_on_siteRwu
MSELECT COUNT(id) FROM metrics WHERE metrics.metric_hash = '64BD7CCE5A95BF00';
���ʖ����	�������d"
page_loadsR��
�SELECT COUNT(DISTINCT CAST((event_timestamp / 1000000 / 60 / 10) AS int)) FROM metrics WHERE metrics.metric_hash = 'AD411B741D0DA012' AND metrics.metric_value > 0;
��袺ص��
������Ơ�"compose_session_countR��
�SELECT COUNT(DISTINCT CAST((event_timestamp / 1000000 / 60 / 10) AS int)) FROM metrics WHERE metrics.metric_hash = 'B4CFE8741404B691' AND metrics.metric_value > 0;
��袺ص��
�풠����"compose_insert_session_countR��
gSELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics WHERE metrics.metric_hash = '534661B278B11BD';
�ٴ�ڥ�7	�����Ù�"nudge_showsR��
hSELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics WHERE metrics.metric_hash = '19E16122849E343B';
�ٴ�ڥ�7	��������"nudge_clicksR��
hSELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics WHERE metrics.metric_hash = '79964621D357AB88';
�ٴ�ڥ�7	��ޚ�đ�y"nudge_site_disablesR��
hSELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics WHERE metrics.metric_hash = '756F6A466879157E';
�ٴ�ڥ�7	������ڷu"nudge_global_disablesR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0) SELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = '534661B278B11BD';
�ٴ�ڥ�7	�����Ù�
 "
nameorigin"nudge_shows_siteR��
�WITH on_site_urlids AS (SELECT DISTINCT url_id FROM urls WHERE instr(url, ?) > 0) SELECT IFNULL(SUM(metrics.metric_value), 0) FROM metrics INNER JOIN on_site_urlids ON metrics.url_id = on_site_urlids.url_id WHERE metrics.metric_hash = '19E16122849E343B';
�ٴ�ڥ�7	��������
 "
nameorigin"nudge_clicks_site�!

  @?ShowDontShow