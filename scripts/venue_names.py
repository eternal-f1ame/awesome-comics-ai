"""Short names for the venue strings that Crossref gives (proceedings or journal titles, event names). First matching rule wins.

The short names are the keys of data/venues.yaml. When a new venue appears, add a rule here and its rank there."""
import json, re, sys

RULES = [
    (r"^arXiv$", "arXiv"),
    (r"Computer Vision and Pattern Recognition Workshops|CVPRW", "CVPR Workshops"),
    (r"Computer Vision and Pattern Recognition", "CVPR"),
    (r"International Conference on Computer Vision Workshops|ICCVW", "ICCV Workshops"),
    (r"International Conference on Computer Vision \(ICCV\)", "ICCV"),
    (r"ECCV \d{4} Workshops", "ECCV Workshops"),
    (r"ECCV \d{4}$", "ECCV"),
    (r"ACCV", "ACCV"),
    (r"Winter Conference on Applications of Computer Vision", "WACV"),
    (r"ICDAR \d{4} Workshops|Document Analysis and Recognition Workshops", "ICDAR Workshops"),
    (r"ICDAR|International Conference on Document Analysis and Recognition", "ICDAR"),
    (r"Document Analysis Systems", "DAS"),
    (r"ICPR 2022 International Workshops", "ICPR Workshops"),
    (r"International Conference on Pattern Recognition \(ICPR\)", "ICPR"),
    (r"Asian Conference on Pattern Recognition", "ACPR"),
    (r"ICIAP", "ICIAP"),
    (r"MANPU", "MANPU"),
    (r"^MultiMedia Modeling$", "MMM"),
    (r"Neural Information Processing Systems", "NeurIPS"),
    (r"AAAI Conference", "AAAI"),
    (r"Findings of the Association for Computational Linguistics: EMNLP", "Findings of EMNLP"),
    (r"Findings of the Association for Computational Linguistics: EACL", "Findings of EACL"),
    (r"Empirical Methods in Natural Language Processing", "EMNLP"),
    (r"European Chapter of the Association for Computational Linguistics", "EACL"),
    (r"North American Chapter", "NAACL"),
    (r"Annual Meeting of the Association for Computational Linguistics", "ACL"),
    (r"Transactions of the Association for Computational Linguistics", "TACL"),
    (r"Conference on Machine Translation", "WMT"),
    (r"^ACM Transactions on Graphics$", "ACM TOG"),
    (r"SIGGRAPH Posters", "SIGGRAPH Posters"),
    (r"SIGGRAPH Asia|^SA ?'\d\d", "SIGGRAPH Asia"),
    (r"SIGGRAPH Conference Papers", "SIGGRAPH"),
    (r"Visualization and Computer Graphics", "TVCG"),
    (r"^IEEE Transactions on Multimedia$", "TMM"),
    (r"^IEEE Transactions on Image Processing$", "TIP"),
    (r"Information Forensics and Security", "TIFS"),
    (r"Circuits and Systems for Video Technology", "TCSVT"),
    (r"Human-Machine Systems", "THMS"),
    (r"Multimedia Computing, Communications, and Applications", "ACM TOMM"),
    (r"Transactions on Accessible Computing", "ACM TACCESS"),
    (r"^IEEE MultiMedia$", "IEEE MultiMedia"),
    (r"Multimedia Tools and Applications", "MTAP"),
    (r"International Journal on Document Analysis and Recognition", "IJDAR"),
    (r"^Computer Graphics Forum$", "CGF"),
    (r"^The Visual Computer$", "The Visual Computer"),
    (r"^Journal of Imaging$", "J. Imaging"),
    (r"Computer Animation and Virtual Worlds", "CAVW"),
    (r"^IEEE Access$", "IEEE Access"),
    (r"^Applied Sciences$", "Applied Sciences"),
    (r"Topics in Cognitive Science", "Topics in Cognitive Science"),
    (r"Information Engineering Express", "Information Engineering Express"),
    (r"^MM ?'\d\d", "ACM MM"),
    (r"MMAsia", "ACM MM Asia"),
    (r"Multimedia and Expo", "ICME"),
    (r"International Symposium on Multimedia", "ISM"),
    (r"Image Processing \(ICIP\)", "ICIP"),
    (r"Visual Communications and Image Processing", "VCIP"),
    (r"Digital Image Computing", "DICTA"),
    (r"Joint Conference on Neural Networks", "IJCNN"),
    (r"CHI EA", "CHI EA"),
    (r"^CHI '\d\d", "CHI"),
    (r"^UIST", "UIST"),
    (r"^IUI", "IUI"),
    (r"Proceedings of the ACM on Human-Computer Interaction", "PACM HCI"),
    (r"SIGCSE", "SIGCSE"),
    (r"Learning Technologies \(LACLO\)", "LACLO"),
    (r"Mindful TEL", "EC-TEL"),
    (r"International Conference on Machine Learning(?! and)", "ICML"),
    (r"International Conference on Learning Representations", "ICLR"),
    (r"International Joint Conference on Artificial Intelligence", "IJCAI"),
    (r"Pattern Analysis and Machine Intelligence", "TPAMI"),
    (r"International Journal of Computer Vision", "IJCV"),
    (r"International Conference on Computational Linguistics|COLING", "COLING"),
    (r"Cognitive Science Society|CogSci", "CogSci"),
    (r"^Interactive Storytelling$", "ICIDS"),
    (r"Symposium on Electronic Art", "ISEA"),
    (r"Agents and Artificial Intelligence", "ICAART"),
    (r"Advanced Image Technology", "IWAIT"),
    (r"Advanced Applied Informatics", "IIAI-AAI"),
    (r"Communication Systems and Network Technologies", "CSNT"),
    (r"Knowledge Engineering and Communication Systems", "ICKECS"),
    (r"ACM TURC", "ACM TURC"),
    (r"Software Engineering, Artificial Intelligence, Networking", "SNPD"),
    (r"Intelligent Signal Processing and Communications", "ISPACS"),
    (r"Information Technology: New Generations", "ITNG"),
    (r"Computer-Aided Industrial Design", "CAIDCD"),
    (r"Granular Computing", "GrC"),
    (r"^Analysis of Images, Social Networks and Texts$", "AIST"),
]


def short(raw):
    for pat, name in RULES:
        if re.search(pat, raw):
            return name
    return None


if __name__ == "__main__":
    raws = json.load(open(sys.argv[1], encoding="utf-8"))
    V = {r: short(r) for r in raws}
    json.dump({k: v for k, v in V.items() if v}, open(sys.argv[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len([v for v in V.values() if v]), "mapped; unmapped:", [k for k, v in V.items() if not v])
